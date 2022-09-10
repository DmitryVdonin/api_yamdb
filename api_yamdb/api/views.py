from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from reviews.models import Category, Genre, Review, Title, User
from reviews.token_generator import confirmation_code

from .permissions import (IsAdmin, IsAdminOrReadOnly,
                          IsOwnerOrModeratorOrReadOnly)
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReadOnlyTitleSerializer,
                          ReviewSerializer, TitleSerializer,
                          UserCreateSerializer, UserSerializer)


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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = IsAdminOrReadOnly,
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    lookup_field = ('slug')


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
    permission_classes = IsAdminOrReadOnly,
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
    lookup_field = ('slug')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = IsAdminOrReadOnly,
    filter_backends = DjangoFilterBackend,
    filterset_fields = ['category__slug', 'genre__slug', 'name', 'year']

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrModeratorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsOwnerOrModeratorOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)

        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
