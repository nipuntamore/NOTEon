from django import forms
from .models import notes

class create_todo(forms.ModelForm):
    class Meta:
        model = notes
        fields = ['title','content','priority','attachment']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter note title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your note here...'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'  # or 'form-select' in Bootstrap 5
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control-file'  # or 'form-control' in Bootstrap 5
            }),
        }
