from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comments, Genre, Review, Title, User


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для view-функции signup"""

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

        elif User.objects.filter(
            ~Q(email=data.get('email')), username=data.get('username')
        ).exists():

            raise serializers.ValidationError('Такой username уже занят')

        elif User.objects.filter(
            ~Q(username=data.get('username')), email=data.get('email')
        ).exists():

            raise serializers.ValidationError('Такой email уже занят')

        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для viewset UserViewSet."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class UserAuthSerializer(serializers.Serializer):
    """Сериализатор для для получения токена через TokenObtainPairView"""

    username = serializers.SlugField(required=True)
    confirmation_code = serializers.CharField(max_length=100, required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data.get('username'))
        if user.confirmation_code == data.get('confirmation_code'):
            refresh = RefreshToken.for_user(user)

            return {
                'access': str(refresh.access_token),
            }

        raise serializers.ValidationError('Неверный confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

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


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
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
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('pub_date',)
