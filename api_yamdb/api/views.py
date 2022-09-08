
from reviews.models import Category, Genre, Title, User
from reviews.token_generator import confirmation_code
from rest_framework import viewsets, generics, mixins
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from reviews.token_generator import confirmation_code
from .permissions import IsAdmin
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer, UserSerializer, UserCreateSerializer


class UserCreateAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        if self.request.method == 'POST':
            if serializer.is_valid():
                username = serializer.validated_data.get('username')
                print(username)
                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                else:
                    user = serializer.save()
                password = confirmation_code.make_token(user)
                print(password)
                user.set_password(password)
                user.is_active = True
                user.save()
                mail_subject = 'Confirm your email account.'
                message = f'user: {user}, confirmation_code: {password}'
                to_email = serializer.data.get('email')
                send_mail(
                    mail_subject,
                    message,
                    'from@example.com',
                    [to_email],
                    fail_silently=False,
                    )


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    lookup_field = 'username'


class UserViewAPI(generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user = self.request.user
        obj = get_object_or_404(User, pk=user.pk)
        self.check_object_permissions(self.request, obj)
        return obj


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = IsAdminOrReadOnly,
    
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
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

