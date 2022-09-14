from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import CHARS_PER_STR
from .validators import validate_year


class User(AbstractUser):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10, choices=USER_ROLES,
        default=USER, verbose_name='Роль',
    )
    email = models.EmailField(max_length=50, unique=True)
    confirmation_code = models.TextField(
        'Код подтверждения',
        blank=True,
    )

    @property
    def is_admin(self):
        return (
            self.role == 'admin'
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Category(models.Model):
    """Категории (типы) произведений."""

    name = models.CharField(
        max_length=255,
        verbose_name='Category',
    )
    slug = models.SlugField(
        verbose_name='Id_Category',
        unique=True,
        max_length=50,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Категории жанров."""

    name = models.CharField(
        max_length=256,
        verbose_name='Genre',
    )
    slug = models.SlugField(
        verbose_name='Id_Genre',
        unique=True,
        max_length=50,
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения, к которым пишут отзывы
    (определённый фильм, книга или песенка)."""

    name = models.CharField(
        max_length=256,
        verbose_name='Title',
        db_index=True,
    )
    year = models.SmallIntegerField(
        verbose_name='Year',
        validators=[validate_year],
    )
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Category',
        related_name='titles',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Genre',
        through='GenreTitle',
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Промежуточная модель GenreTitle(ЖанрПроизведение)."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Genre',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Title',
    )

    def __str__(self):
        return f'{self.title}, {self.genre}'


class Review(models.Model):
    """Модель Review(отзыв)."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews',
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='автор_отзыва',
        related_name='reviews',
    )
    score = models.SmallIntegerField(
        verbose_name='Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'],
                name='unique_review_per_title',
            ),
        ]

    def __str__(self):
        return self.text[:CHARS_PER_STR]


class Comments(models.Model):
    """Модель Comments(комментарии)."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments',
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return self.text[:CHARS_PER_STR]
