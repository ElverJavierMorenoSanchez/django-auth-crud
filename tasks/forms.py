from django import forms
from .models import Task


class Singup(forms.Form):
    username = forms.CharField(label="Username",
                               max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(label="Password", min_length=8,
                               widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}))


class CreateTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control mb-3"}),
            'description': forms.Textarea(attrs={'class': "form-control mb-3"}),
            'important': forms.CheckboxInput(attrs={'class': "form-check-input mb-3"})
        }
