from django import forms
from django.core.exceptions import ValidationError

from .models import *
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
            'is_published',
            'slug',
        ]

    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), label="Текст")
    title = forms.TextInput(attrs={'class': 'form-input'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"

    # простой валидатор длины поля начинается со слова clean_
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title