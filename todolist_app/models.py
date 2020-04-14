from django.db import models
from django.conf import settings


# Create your models here.


class Priority(models.Model):
    name = models.CharField(max_length=20)
    orders = models.IntegerField()


class Todo(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned",
    )
    done = models.BooleanField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="updated",
    )
    priority = models.ForeignKey(
        Priority,
        on_delete=models.CASCADE,
        related_name="priority",
    )
    due_Date = models.DateField(auto_now_add=True)
