from django import forms
from django.core.exceptions import ValidationError

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *


class AddReplyForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 10}), label='Текст отклика')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'category',
            # 'author',
            'photo',
            # 'replies',
            'is_published',
            # 'slug',
        ]

    content = forms.CharField(widget=CKEditorUploadingWidget(attrs={'cols': 80, 'rows': 30}), label="Текст")
    # TODO length title in PostForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"

    # простой валидатор  поля начинается со слова clean_имя_поля, после идет проверка ввалидаторе clean
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 64:
            raise ValidationError('Длина превышает 64 символов')

        return title
