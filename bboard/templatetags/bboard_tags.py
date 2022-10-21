# Тэги введены для использования по необходимости (могут и не быть использованы)

from django import template
from bboard.models import *


register = template.Library()

@register.inclusion_tag('bboard/list_replies.html')
def show_replies(sort=None):
    if not sort:
        replies = Reply.objects.all()
    else:
        replies = Reply.objects.all().order_by(sort)

    return {"replies": replies}


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
