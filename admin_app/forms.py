from django import forms
from .models import Article
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from froala_editor.widgets import FroalaEditor

class Article_form(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'thumbnail']
        widgets = {
            'title': forms.TextInput(
            attrs={
                'class': 'form-control position-relative',
                'placeholder': 'Article title',
                'data-parsley-trigger': 'change',
                'required': 'required',
                'id': 'title-icon'
            }
        ),
            'content': FroalaEditor(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Title'
        self.fields['content'].label = 'Content'
        self.fields['thumbnail'].label = 'Thumbnail'

class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name", "required": "required"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name", "required": "required"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email", "required": "required"}),
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username", "required": "required"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = True
            
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})