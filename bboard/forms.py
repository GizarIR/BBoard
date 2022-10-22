from django import forms
from django.core.exceptions import ValidationError

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *

class AddReplyForm(forms.Form):
    # title = forms.CharField(widget=forms.TextInput(), disabled=True)
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 15}), disabled=True, label='Объявление')
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), disabled=True, label='Текст отклика')
    is_approved = forms.BooleanField(label='Разрешено')

# class AddReplyForm(forms.ModelForm):
#     class Meta:
#         model = Reply
#         fields = "__all__"



class AddPostForm(forms.ModelForm):
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

    # content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), label="Текст")
    content = forms.CharField(widget=CKEditorUploadingWidget(attrs={'cols': 80, 'rows': 30}), label="Текст")
    title = forms.TextInput(attrs={'class': 'form-input'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Категория не выбрана"

    # простой валидатор  поля начинается со слова clean_имя_поля, после идет проверка ввалидаторе clean
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title
