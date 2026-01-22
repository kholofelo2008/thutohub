from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('learner', 'Learner'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='learner')
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Useful for SA parents
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    GRADE_CHOICES = (
        ('grade_r', 'Grade R'),
        ('grade_1', 'Grade 1'),
        ('grade_2', 'Grade 2'),
        ('grade_3', 'Grade 3'),
        ('grade_4', 'Grade 4'),
        ('grade_5', 'Grade 5'),
        ('grade_6', 'Grade 6'),
        ('grade_7', 'Grade 7'),
        ('grade_8', 'Grade 8'),
        ('grade_9', 'Grade 9'),
        ('grade_10', 'Grade 10'),
        ('grade_11', 'Grade 11'),
        ('grade_12', 'Grade 12'),
    )

    grade = models.CharField(
        max_length=20,
        choices=GRADE_CHOICES,
        blank=True,
        null=True,
        help_text="Grade for learners (leave blank for other roles)"
    )
    
    # For learners/parents: link relationships later
    # e.g. parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_teacher(self):
        return self.role == 'teacher'
    
    @property
    def is_parent(self):
        return self.role == 'parent'
    
    @property
    def is_learner(self):
        return self.role == 'learner'
