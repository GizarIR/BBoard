from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import *

User = get_user_model()


class OneTimeCodeAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'user',
    ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # pass
    list_display = ['username', 'is_staff', 'email', 'email_verify']
    list_filter = ['username',]
    search_fields = ['username',]

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

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(OneTimeCode, OneTimeCodeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Reply, ReplyAdmin)

