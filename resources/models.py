from django.db import models
from accounts.models import User

class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='resources/%Y/%m/%d/')  # organizes by date
    subject = models.CharField(max_length=100, blank=True)
    grade = models.CharField(max_length=20, choices=User.GRADE_CHOICES,
    blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title