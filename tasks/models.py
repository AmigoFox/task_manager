from django.conf import settings
from django.db import models
from django.utils import timezone


@property
def is_overdue(self):
    return not self.completed and self.due_date is not None and self.due_date < timezone.now()

class Task(models.Model):
    LOW = 'low'
    NORMAL = 'normal'
    HIGH = 'high'
    PRIORITY_CHOICES = [
        (LOW, 'Низкий'),
        (NORMAL, 'Обычный'),
        (HIGH, 'Высокий'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=NORMAL)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title