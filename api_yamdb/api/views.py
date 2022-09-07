from reviews.models import User
from reviews.token_generator import confirmation_code
from rest_framework import viewsets, generics, mixins
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, UserCreateSerializer, UserTokenObtainSerializer
from .permissions import IsAdmin


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
                #mail_subject = 'Confirm your email account.'
                #message = f'user: {user}, password: {password}'
                #to_email = serializer.data.get('email')
                #send_mail(
                    #mail_subject,
                    #message,
                    #'from@example.com',
                    #['to@example.com'],
                    #fail_silently=False,
                    #)


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )

    def get_object(self):
        username = self.kwargs.get('pk')
        print(self.kwargs)
        obj = get_object_or_404(User, username=username)
        self.check_object_permissions(self.request, obj)
        return obj


class UserViewSet(generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user = self.request.user
        obj = get_object_or_404(User, pk=user.pk)
        self.check_object_permissions(self.request, obj)
        return obj

class TokenObtain(TokenObtainPairView):
    serializer_class = UserTokenObtainSerializer
