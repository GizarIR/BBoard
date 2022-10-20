from django.contrib import admin
from .models import *
from unidecode import unidecode

# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['author_user', 'one_time_code', 'time_created',]
    list_filter = ['author_user',]
    search_fields = ['author_user', 'one_time_code', 'time_created']

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]
    prepopulated_fields = {"slug": ("name",)}

class PostAdmin(admin.ModelAdmin):
    """Наследуем класс Django, данное наследование позволяет настроить Админку для модели Post"""
    list_display = [
        'title',
        # 'content',
        'category',
        'author',
        'photo',
        'time_create',
        'time_update',
        'is_created',
        'replies',
        'slug',
    ]
    list_filter = [
        'category',
        'author',
        'time_create',
        'time_update',
    ]
    list_editable = ('is_created',)
    search_fields = ['title', 'content']
    prepopulated_fields = {"slug": ("title","category")}
    list_per_page = 10

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'time_create', 'time_update', 'text', 'is_approved',]
    list_filter = ['author', 'time_create', 'time_update', 'is_approved',]
    list_editable = ('is_approved',)
    search_fields = ['text',]
    list_per_page = 10

admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Reply, ReplyAdmin)

