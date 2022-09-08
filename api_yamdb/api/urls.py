from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserAuthSerializer
from .views import AdminUserViewSet, UserCreateAPI, CategoryViewSet, GenreViewSet, TitleViewSet, AdminUserViewSet, UserViewAPI

app_name = 'reviews'

v1_router = routers.DefaultRouter()
v1_router.register('users', AdminUserViewSet)
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('genries', GenreViewSet, basename='genries')

urlpatterns = [
    path('v1/users/me/', UserViewAPI.as_view()),
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(serializer_class=UserAuthSerializer),
        name='token_obtain_pair'
        ),
    path('v1/auth/signup/', UserCreateAPI.as_view()),
    path('v1/', include(v1_router.urls)),
]
