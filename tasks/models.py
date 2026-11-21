from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    """
    Task model representing a user's personal task.
    Enforces server-side data ownership via ForeignKey to User.
    """
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="tasks"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['completed', 'due_date', '-created_at']

    def __str__(self):
        return self.title
