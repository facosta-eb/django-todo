from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Priority, Todo

class TestLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()

    def test_login_valid(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': '12345'}, follow=True)
        self.assertRedirects(response, '/home/')
        self.assertTrue(response.context["user"].is_authenticated)

    def test_login_invalid(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'nopnop'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)


class TestCreateAndUpdate(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()
        self.p = Priority.objects.create(name="Urgent", orders=3)
        self.p.save()

    def test_create_todo(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create/', {
            "title": 'tarea3',
            "assigned_user": self.user.id,
            "description": 'cosas',
            'done': True,
            "priority": 1,
            }, follow=True)
        todo_id = max(Todo.objects.all().values_list("id"))[0]
        self.assertRedirects(response, f'/view/{todo_id}')
        self.assertTrue(Todo.objects.filter(id=todo_id))
    
    def test_create_todo_invalid(self):
        self.client.login(username='testuser', password='12345')
        before_items = len(Todo.objects.all())
        response = self.client.post('/create/', {
            "title": 'tarea3',
            "assigned_user": self.user.id,
            "description": 'cosas',
            'done': True,
            "priority": "not a valid choice",
            }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Todo.objects.all()), before_items)
        

    def test_update_todo(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create/', {
            "title": 'tarea3',
            "assigned_user": self.user.id,
            "description": 'cosas',
            'done': True,
            "priority": 1,
            }, follow=True)
        todo_id = max(Todo.objects.all().values_list("id"))[0]
        response = self.client.post(f'/update/{todo_id}', {
            "title": 'tarea3',
            "description": 'cosas muchas cosas',
            'done': False,
            "priority": self.p.id,
            }, follow=True)
        item = Todo.objects.get(id=todo_id)
        self.assertEqual(item.title, "tarea3")
        self.assertEqual(item.description, "cosas muchas cosas")
        self.assertFalse(item.done)
        self.assertRedirects(response, f'/view/{todo_id}')


class TestRedirects(TestCase):


    def test_redirect_from_home(self):
        response = self.client.get('/home', follow=True)
        self.assertRedirects(response, '/login/', status_code=301)

# Create your tests here.
