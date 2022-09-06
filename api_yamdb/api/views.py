from reviews.models import Category, Genre, Title, User
from reviews.token_generator import confirmation_code
from django.core.mail import send_mail
from rest_framework import viewsets
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
# from .permissions import IsAdminOrReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer)::
    if request.method == 'POST':
        if serializer.is_valid():
            user = serializer.save(commit=False)
            password = confirmation_code.make_token(user)
            user.password = password
            user.is_active = False
            user.save()
            mail_subject = 'Confirm your email account.'
            message = f'user: {user}, password: {password}
            to_email = serializer.data.get('email')
            send_mail(
                mail_subject,
                message,
                'from@example.com',
                ['to@example.com'],
                fail_silently=False,
                )
                
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
