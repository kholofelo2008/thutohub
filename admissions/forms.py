from django import forms
from .models import AdmissionApplication

class AdmissionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdmissionApplication
        fields = [
            'child_full_name', 'child_gender', 'child_date_of_birth', 'child_grade_applied',
            'current_school', 'residential_address', 'parent_phone', 'parent_email',
            'birth_certificate', 'proof_of_residence', 'immunization_record',
            'report_card', 'additional_docs'
        ]
        widgets = {
            'child_date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'residential_address': forms.Textarea(attrs={'rows': 3}),
            'admin_notes': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'child_full_name': "Child's Full Name",
            'child_date_of_birth': "Date of Birth",
            'child_grade_applied': "Grade Applying For",
        }