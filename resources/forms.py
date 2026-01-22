from django import forms
from .models import Resource

class ResourceUploadForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file', 'subject', 'grade']  # ← no video_url here!
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }