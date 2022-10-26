from django.db.models import Count

from .models import *

menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "Добавить объявление", 'url_name': 'add_page'},
        {'title': "Личный кабинет", 'url_name': 'replies_list_search'},
        {'title': "Выйти", 'url_name': 'logout'},
        {'title': "Войти", 'url_name': 'login'},
        ]


class DataMixin:
    paginate_by = 2
    def get_user_context(self, **kwargs):
        context = kwargs
        # categories = Category.objects.all()
        categories =  Category.objects.annotate(Count('post'))

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            for i in range(3):
                user_menu.pop(1)
        else:
            user_menu.pop(4)


        context['menu'] = user_menu
        context['categories'] = categories
        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context