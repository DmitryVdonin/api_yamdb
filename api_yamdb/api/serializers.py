from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)

    def run_validators(self, value):
        for validator in self.validators:
            if isinstance(validator, validators.UniqueTogetherValidator):
                self.validators.remove(validator)
        super(UserCreateSerializer, self).run_validators(value)

    def create(self, validated_data):
        instance, _ = models.User.objects.get_or_create(**validated_data)
        return instance

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Запрещенный username')
        return data
        

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Запрещенный username')
        return data

        
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
