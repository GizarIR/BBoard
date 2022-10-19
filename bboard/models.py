from django.contrib.auth.models import User
from django.db import models
from tinymce import models as tinymce_models
from django.urls import reverse

# Create your models here.

class Author(models.Model):
    """
    Модель Author - объекты всех авторов, поля:
        - cвязь «один к одному», с встроенной моделью пользователей User;
    """
    author_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Author",
    )
    one_time_code = models.CharField(max_length=255)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author_user.username}'

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

class Category(models.Model):
    """
    Модель Category, поля:
        - название категории, поле уникально
        - slug
    """
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Category',
        help_text='Name of category - 64 characters',
    )
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return f"{self.name.title()}"

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Reply(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name="Author")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}: {self.text}"

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = tinymce_models.HTMLField(verbose_name="Текст объявления")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")
    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name="Автор")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото заголовка", blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_created = models.BooleanField(default=True)
    replies = models.ForeignKey('Reply', on_delete=models.CASCADE, verbose_name="Отклики", blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    def __str__(self):
        # return f"{self.create_date:%Y-%m-%d %H:%M} --- {self.header_post}"
        return f"{self.id}: {self.title}"

    def get_absolute_url(self):
        # post это имя маршрута
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'

