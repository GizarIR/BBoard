from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from unidecode import unidecode
from ckeditor_uploader.fields import RichTextUploadingField


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
        "email address",
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
        # reply  - name of route
        return reverse('reply', kwargs={'pk': self.pk})

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
        return f"{self.id}: {self.title}"

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
