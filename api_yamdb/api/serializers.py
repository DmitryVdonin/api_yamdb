from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, User


class UserCreateSerializer(serializers.ModelSerializer):

    def is_valid(self, raise_exception=False):
        if hasattr(self, 'initial_data'):
            try:
                obj = User.objects.get(
                    username=self.initial_data.get('username')
                    )
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
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
            )

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Запрещенный username')
        return data


class UserAuthSerializer(serializers.Serializer):
    username = serializers.SlugField()
    confirmation_code = serializers.CharField(max_length=100)

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        if user.check_password(data.get('confirmation_code')):
            refresh = RefreshToken.for_user(user)
            return {
                'access': str(refresh.access_token),
            }
        return 'self.get_tokens_for_user(user)'

        
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
