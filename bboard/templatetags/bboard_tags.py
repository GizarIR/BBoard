# Тэги введены для использования по необходимости (могут и не быть использованы)

from django import template
from bboard.models import *


register = template.Library()

@register.inclusion_tag('bboard/list_replies.html')
def show_replies(sort=None, throught_slug=False, post_id=None):
    if throught_slug:
        post_id = Post.objects.get(slug=post_id).pk
    if post_id is not None:
        if not sort:
            replies = Reply.objects.filter(post=post_id, is_approved=True)
        else:
            replies = Reply.objects.filter(post=post_id, is_approved=True).order_by(sort)
        return {"replies": replies}
    else:
        return {"replies": {}}


@register.inclusion_tag('bboard/show_post.html')
def show_post(slug_post=None):
    if slug_post is not None:
        posts = Post.objects.filter(slug=slug_post, is_published=True)
        return {"posts": posts}
    else:
        return {"posts": {}}

# # Простые тэги позвляют включить в шаблон любую переменную без использования функций или классов во вьюшках
# # Пример использования в шаблоне {% getcats 'dd' %}
# @register.simple_tag(name='getcats')
# def get_categories(filter=None):
#     if not filter:
#         return Category.objects.all()
#     else:
#         return Category.objects.get(slug=filter)
#
# # данный тип тэгов позволяет включить фрагмент кода с нужными переменными
# # для использования в шаблоне: {% show_categories cat_selected=cat_selected %}
# @register.inclusion_tag('bboard/list_categories.html')
# def show_categories(sort=None, cat_selected=0):
#     if not sort:
#         cats = Category.objects.all()
#     else:
#         cats = Category.objects.all().order_by(sort)
#
#     return {"cats": cats, "cat_selected": cat_selected}
