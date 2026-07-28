from django.forms import forms
from .models import notes

class create_todo(forms.ModelForm):
    class Meta:
        model = notes
        fields = ['title','content','priority','attachment']
        