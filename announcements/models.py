from django.db import models
from accounts.models import User

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    grade = models.CharField(max_length=20, choices=User.GRADE_CHOICES,
    blank=True, null=True)
    # Optional: target audience (all, parents only, specific grade)
    target_role = models.CharField(max_length=20, choices=[('all', 'All'), ('parents', 'Parents'), ('learners', 'Learners')], default='all')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title