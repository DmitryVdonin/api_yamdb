import datetime

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comments, Genre, Review, Title, User


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

        raise serializers.ValidationError('This field must be an even number.')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year'),
                message=(
                    'Произведение с таким названием и годом уже существует.'
                )
            )
        ]

    def validate_year(self, value):
        now_year = datetime.datetime.now().year
        if not (now_year >= value):
            raise serializers.ValidationError(
                'Проверьте год выпуска произведения!')

        return value


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        avg_rating = Title.objects.get(id=obj.id).reviews.aggregate(
            Avg('score')
        )['score__avg']
        if avg_rating:

            return round(avg_rating)
        else:

            return None


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('pub_date',)

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context.get('view').kwargs['title_id']
            if Review.objects.filter(author=user, title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв об этом произведении'
                )

        return attrs


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comments."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('pub_date',)
