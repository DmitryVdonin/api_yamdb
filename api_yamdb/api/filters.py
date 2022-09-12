import django_filters

from reviews.models import Title
from django.db import models
from django_filters import filters


class TitleFilter(django_filters.FilterSet):
    category = filters.CharFilter(
        field_name='category__slug'
    )
    genre = filters.CharFilter(
        field_name='genre__slug'
    )

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }
