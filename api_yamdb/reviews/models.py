from django.contrib.auth.models import AbstractUser
from django.db import models
from .constants import CHARS_PER_STR


ROLES = (
    ('user', 'user'),
    ('moderator','moderator'),
    ('admin', 'admin'),
)

class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(max_length=10, choices=ROLES, default='user', verbose_name='Роль')


CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)


# Для слаг добавить фильтр на регексп? в редоке посмотреть
class Category(models.Model):
    """Модель Category(Категория)."""

    name = models.CharField(
        max_length=256,
        verbose_name='Category',
    )
    slug = models.SlugField(
        verbose_name='Id_Category',
        unique=True,
        max_length=50
    )

    def __str__(self):
        return self.name


# Для слаг добавить фильтр на регексп? в редоке посмотреть
class Genre(models.Model):
    """Модель Genre(Жанр)."""

    name = models.CharField(
        max_length=256,
        verbose_name='Genre',
    )
    slug = models.SlugField(
        verbose_name='Id_Genre',
        unique=True,
        max_length=50
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель Title(Произведение)."""

    name = models.CharField(
        max_length=256,
        verbose_name='Title',
    )
    year = models.IntegerField(
        verbose_name='Year'
    )
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Category',
        related_name='category',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Genre',
        through='GenreTitle'
    )
    rating = models.IntegerField(
        verbose_name='Rating',
        null=True,
        default=None
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Промежуточная модель GenreTitle(ЖанрПроизведение)."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Genre'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Title'
    )

    def __str__(self):
        return f'{self.title}, {self.genre}'


class Review(models.Model):
    """Модель Review(отзыв)."""

    title_id = models.ForeignKey(
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
    score = models.IntegerField(choices=CHOICES, verbose_name='Рейтинг')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return self.text[:CHARS_PER_STR]


class Comments(models.Model):
    """Модель Comments(комментарии)."""

    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return self.text[:CHARS_PER_STR]
