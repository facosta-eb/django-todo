from django.urls import path, include

from .views import (
    TodoListView,
    TodoCreateView,
    TodoDeleteView,
    TodoUpdateView,
    TodoReassignView,
    TodoDetailView,
    TodoHomeView,
    )


urlpatterns = [
    path('', TodoListView.as_view(), name='todo_list'),
    path('home/', TodoHomeView.as_view(), name='todo_home'),
    path('create/', TodoCreateView.as_view(), name='todo_create'),
    path('delete/<pk>', TodoDeleteView.as_view(), name='todo_delete'),
    path('update/<pk>', TodoUpdateView.as_view(), name='todo_update'),
    path('reassign/<pk>', TodoReassignView.as_view(), name='todo_reassign'),
    path('view/<pk>', TodoDetailView.as_view(), name='todo_detail'),
    path('', include('django.contrib.auth.urls')),  # new
]
