from reviews.models import Category, Genre, Title
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    # category = serializers.SlugRelatedField(
    #     slug_field='slug',
    #     queryset=Category.objects.all()
    # )
    # genre = serializers.SlugRelatedField(
    #     slug_field='name',
    #     many=True,
    #     queryset=Genre.objects.all()
    # )

    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    '''
    Добавить rating = среднее значение score из модели Review
    # from reviews.models import Review
    # from django.db.models import Avg
    # queryset=Review.objects.aggregate(Avg('score'))
    '''

    class Meta:
        model = Title
        fields = '__all__'
