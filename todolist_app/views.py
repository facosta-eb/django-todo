from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Todo


class GetObjectMixin():
    def get_object(self):
        user = self.request.user
        item = super().get_object()
        if user.id != item.assigned_user.id:
            raise PermissionDenied
        return item


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    login_url = '/login'
    redirect_field_name = ''

class TodoHomeView(GetObjectMixin, LoginRequiredMixin, ListView):
    model = Todo
    template_name_suffix = '_home'
    username = None
    login_url = '/login'
    redirect_field_name = ''

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Todo.objects.filter(assigned_user=self.request.user)


class TodoCreateView(GetObjectMixin, LoginRequiredMixin, CreateView):
    model = Todo
    fields = [
        'assigned_user',
        'title',
        'description',
        'priority',
        'done',
        ]
    success_url = reverse_lazy('todo_detail')
    login_url = '/login'
    redirect_field_name = ''

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('todo_detail', args=(self.object.id,))


class TodoUpdateView(GetObjectMixin, LoginRequiredMixin, UpdateView):
    model = Todo
    fields = [
        'title',
        'description',
        'priority',
        'done',
        ]
    login_url = '/login'
    redirect_field_name = ''
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('todo_detail', args=(self.object.id,))

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class TodoDeleteView(GetObjectMixin, LoginRequiredMixin, DeleteView):
    model = Todo
    fields = ['title']
    success_url = reverse_lazy('todo_home')
    login_url = '/login'
    redirect_field_name = ''


class TodoReassignView(GetObjectMixin, LoginRequiredMixin, UpdateView):
    model = Todo
    fields = [
        'assigned_user',
        ]
    success_url = reverse_lazy('todo_home')
    template_name_suffix = '_reassign_form'
    login_url = '/login'
    redirect_field_name = ''


class TodoDetailView(GetObjectMixin, LoginRequiredMixin, DetailView):
    model = Todo
    login_url = '/login'
    redirect_field_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Create your views here.
