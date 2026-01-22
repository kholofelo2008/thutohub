from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'target_role']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }
        
