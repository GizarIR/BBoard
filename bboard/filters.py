from django_filters import CharFilter, ModelMultipleChoiceFilter, BooleanFilter
from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):

    reply__icontains = CharFilter(
        field_name='text',
        lookup_expr='icontains',
        label='Текст отклика содержит ',
    )

    for_post = ModelMultipleChoiceFilter(
        field_name='post',
        queryset=Post.objects.all(),
        label='Объявление ',
        conjoined=False,
    )

    for_is_approved = BooleanFilter(
        field_name='is_approved',
        label='Разрешено ',
    )

    class Meta:
        model = Post
        fields = [
            'for_post',
            'reply__icontains',
            "for_is_approved",
        ]
