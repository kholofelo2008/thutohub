from django.db import models
from accounts.models import User
from django.utils import timezone

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('waitlist', 'Waitlisted'),
)

class AdmissionApplication(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'parent'})
    child_full_name = models.CharField(max_length=150)
    child_gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    child_date_of_birth = models.DateField()
    child_grade_applied = models.CharField(max_length=50)  # e.g. "Grade R", "Grade 8"
    current_school = models.CharField(max_length=200, blank=True)
    residential_address = models.TextField()
    parent_phone = models.CharField(max_length=15)
    parent_email = models.EmailField(blank=True)
    
    # Documents
    birth_certificate = models.FileField(upload_to='admissions/birth/%Y/%m/', blank=True, null=True)
    proof_of_residence = models.FileField(upload_to='admissions/residence/%Y/%m/', blank=True, null=True)
    immunization_record = models.FileField(upload_to='admissions/immun/%Y/%m/', blank=True, null=True)
    report_card = models.FileField(upload_to='admissions/report/%Y/%m/', blank=True, null=True)
    additional_docs = models.FileField(upload_to='admissions/extra/%Y/%m/', blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(default=timezone.now)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_admissions')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.child_full_name} ({self.child_grade_applied}) - {self.parent.username}"

    class Meta:
        ordering = ['-submitted_at']