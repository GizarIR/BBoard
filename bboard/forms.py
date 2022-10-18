from django import forms
from .models import *
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category',
            'author',
            'photo',
            'replies',
            'slug',
        ]
        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-input'}),
        #     'content': forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30})),
        # }
