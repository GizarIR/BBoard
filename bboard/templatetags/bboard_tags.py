from django import template
from bboard.models import *


register = template.Library()

# Простые тэги позвляют включиь в шаблон любую переменную без использования функций или классов во вьюшках
# Пример использования в шаблоне {% getcats 'dd' %}
@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.get(slug=filter)

# данный тип тэгов позволяет включить фрагмент кода с нужными переменными
@register.inclusion_tag('bboard/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.all().order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}

