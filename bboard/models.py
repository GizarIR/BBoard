from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
# from tinymce import models as tinymce_models
from django.urls import reverse

from unidecode import unidecode
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _


# class Author(models.Model):
#     """
#     Модель Author - объекты всех авторов, поля:
#         - cвязь «один к одному», с встроенной моделью пользователей User;
#     """
#     author_user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name="Автор",
#     )
#     one_time_code = models.CharField(max_length=255)
#     time_created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.author_user.username}'
#
#     class Meta:
#         verbose_name = 'Автор'
#         verbose_name_plural = 'Авторы'

class OneTimeCode(models.Model):
    code = models.CharField(
        max_length=12,
        verbose_name='Одноразовый код',
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        verbose_name="Пользователь")
    class Meta:
        verbose_name = 'Одноразовый код'
        verbose_name_plural = 'Одноразовые коды'


class User(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True
    )

    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Category(models.Model):
    """
    Модель Category, поля:
        - название категории, поле уникально
        - slug
    """
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Категория',
        help_text='Имя категории длинной не более 64 символов ',
    )
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return f"{self.name.title()}"

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Reply(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Пользователь")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name="Пост")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True, verbose_name="Текс")
    is_approved = models.BooleanField(default=False, verbose_name="Разрешено")

    def __str__(self):
        return f"{self.id}: {self.text}"

    def get_absolute_url(self):
        # reply это имя маршрута
        return reverse('reply', kwargs={'pk': self.pk}) # for view

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = RichTextUploadingField(blank=True, default='', verbose_name="Текст")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Пользователь")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото заголовка", blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_created = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовать")

    def __str__(self):
        # return f"{self.create_date:%Y-%m-%d %H:%M} --- {self.header_post}"
        return f"{self.id}: {self.title}"

    def get_absolute_url(self):
        # post это имя маршрута
        # return reverse('post', kwargs={'post_slug': self.slug}) # для функции
        return reverse('post', kwargs={'slug': self.slug}) # for view

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

