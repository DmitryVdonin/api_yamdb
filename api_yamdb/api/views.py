from rest_framework import viewsets
from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
# from .permissions import IsAdminOrReadOnly


'''
Добавить поиск по категории
+ Добавить пагинацию
+ Пермишен Только админ или чтение
'''
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = IsAdminOrReadOnly,


'''
Добавить поиск по жанру
+ Добавить пагинацию
+ Пермишен Только админ или чтение
'''
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = IsAdminOrReadOnly,


'''
Добавить фильтры по полю slug категории
Добавить фильтры по полю slug жанра
Добавить фильтр по названию произведения
Добавить фильтр по году
+ Добавить пагинацию
+ Пермишен Только админ или чтение
'''
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = IsAdminOrReadOnly,
