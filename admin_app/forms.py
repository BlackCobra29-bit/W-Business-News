from django import forms
from .models import Article
from froala_editor.widgets import FroalaEditor

class Article_form(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'thumbnail']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter title',
                    'data-parsley-trigger': 'change',
                    'required': True
                }
            ),
            'content': FroalaEditor(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Title'
        self.fields['content'].label = 'Content'
        self.fields['thumbnail'].label = 'Thumbnail'