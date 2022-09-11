from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from reviews.models import User
from reviews.token_generator import confirmation_code

from .permissions import IsAdmin
from .serializers import UserCreateSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request): 
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        print(username)
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                return Response(serializer.errors, status=400)
        else:
            user = serializer.save()
        password = confirmation_code.make_token(user)
        print(password)
        user.set_password(password)
        user.is_active = True
        user.save()
        mail_subject = 'Confirm your email account.'
        message = f'user: {user}, confirmation_code: {password}'
        user.email_user(mail_subject, message)
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)


class UserViewAPI(generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user = self.request.user
        obj = get_object_or_404(User, pk=user.pk)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = request.data
        if 'role' in data:
            data._mutable = True
            data.pop('role')
            data._mutable = False
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
