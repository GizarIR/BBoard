from django_filters import CharFilter, ModelChoiceFilter, ModelMultipleChoiceFilter, DateFilter, BooleanFilter
from django_filters import FilterSet
from .models import Post, User
import django.forms


class PostFilter(FilterSet):
    reply__icontains = CharFilter(
        field_name='text',
        lookup_expr='icontains',
        label= 'Текст отклика содержит ', # Заголовок
    )

    # Автор
    from_author = ModelChoiceFilter(
        field_name='username',
        queryset=User.objects.all(),
        label='Пользователь ',
        empty_label='Любое',  # любая
    )

    # Публикация
    for_post =  ModelMultipleChoiceFilter(
        field_name='post',
        queryset=Post.objects.all(),
        label='Объявление ',
        conjoined=False,
    )

    # Создадим фильтр Категория
    for_is_approved = BooleanFilter(
        field_name='is_approved',
        label='Разрешено ',
        # empty_label = 'Все',
    )

    # Создадим на странице фильтр дат, для его отрисовки используем виджет
    # create_date = DateFilter(
    #     label=_('Later dates'), #Позже даты
    #     lookup_expr='gte',
    #     # виджеты - это такие поля, которые реализованы через отдельные классы и позволяют за счет настройки их атрибутов
    #     # получать визуализацию специфических полей фильтров без отдельной прорисовки их в html шаблонах
    #     widget=django.forms.DateInput(
    #         attrs={
    #             'type':'date',
    #             # 'format': '%d-%m-%Y', # возможный атрибут
    #         }
    #     )
    # )


    class Meta:
        """Класс Meta позволяет определять порядок полей и регулярное выражение для поиска на странице
         Если нет других описаний полей поиска, то поля отрисуются автоматически cjukfсно описанию в даном классе"""
        model = Post
        fields = [
            'from_author', # в задании не требуется
            'for_post',
            'reply__icontains',
            "for_is_approved",
            # 'create_date',
        ]

