from posixpath import basename
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet, AdminUserViewSet, UserCreateAPI, TokenObtain
from .serializers import UserTokenObtainSerializer

app_name = 'reviews'

v1_router = routers.DefaultRouter()
v1_router.register('users', AdminUserViewSet)
v1_router.register(
    r'users/(?P<username>[\w.@+-]+)',
    AdminUserViewSet,
    basename='users')

urlpatterns = [
    path('v1/users/me/', UserViewSet.as_view()),
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/signup/', UserCreateAPI.as_view()),
    path('v1/', include(v1_router.urls)),
]
