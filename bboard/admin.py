from django.contrib import admin
from .models import *
from unidecode import unidecode


# class UserAdmin(admin.ModelAdmin):
#     list_display = ['user',]
#     list_filter = ['user',]
#     search_fields = ['user',]

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
        # 'user',
        'photo',
        'time_create',
        'time_update',
        'is_created',
        'slug',
    ]
    list_filter = [
        'category',
        # 'user',
        'time_create',
        'time_update',
    ]
    list_editable = ('is_created',)
    search_fields = ['title', 'content']
    prepopulated_fields = {"slug": ("title","category")}
    list_per_page = 10

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['post', 'time_create', 'time_update', 'text', 'is_approved',] #'user'
    list_filter = ['post', 'time_create', 'time_update', 'is_approved',] #'user'
    list_editable = ('is_approved',)
    search_fields = ['text',]
    list_per_page = 10

# admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Reply, ReplyAdmin)

