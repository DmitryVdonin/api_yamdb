from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserAuthSerializer
from .views import AdminUserViewSet, UserViewAPI, signup

app_name = 'reviews'

v1_router = routers.DefaultRouter()
v1_router.register('users', AdminUserViewSet)

urlpatterns = [
    path('v1/users/me/', UserViewAPI.as_view()),
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(serializer_class=UserAuthSerializer),
        name='token_obtain_pair'
        ),
    path('v1/auth/signup/', signup),
    path('v1/', include(v1_router.urls)),
]
