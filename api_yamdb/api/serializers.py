from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from reviews.models import Category, Genre, Title, User, Review, Comments
from django.contrib.auth import authenticate
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login


class UserCreateSerializer(serializers.ModelSerializer):

    def is_valid(self, raise_exception=False):
        if hasattr(self, 'initial_data'):
            try:
                obj = User.objects.get(username=self.initial_data.get('username'))
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                return super().is_valid(raise_exception)
            else:
                self.instance = obj
                return super().is_valid(raise_exception)
        else:
            return super().is_valid(raise_exception)

    class Meta:
        model = User
        fields = ('username', 'email',)

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


class UserTokenObtainSerializer(TokenObtainPairSerializer):
    #confirmation_code = serializers.CharField(source='password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("init")

        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()
        print("init1")

    def validate(self, attrs):
        print('validate')
        user = get_object_or_404(User, username=attrs['username'])
        print(user.pk)
        print(attrs['confirmation_code'])
        self.user = authenticate(username=attrs['username'], password=attrs['confirmation_code'])
        print(bool(self.user))
        
        data = {}

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

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


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title_id = serializers.HiddenField(default=None)

    class Meta:
        model = Review
        fields = ('id', 'title_id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('pub_date',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title_id', 'author'),
                message='Вы уже оставили отзыв об этом произведении',
            )
        ]