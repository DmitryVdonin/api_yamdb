from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserAuthSerializer
from .views import (UserViewSet, CategoryViewSet, CommentsViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, signup)


app_name = 'reviews'

v1_router = routers.DefaultRouter()
v1_router.register('users', UserViewSet)
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews',
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments',
)


auth_urlpatterns = [
    path(
        'token/',
        TokenObtainPairView.as_view(serializer_class=UserAuthSerializer),
        name='token_obtain_pair'
    ),
    path('signup/', signup),
]
urlpatterns = [
    path('v1/users/me/', UserViewAPI.as_view()),
    path('v1/auth/', include(auth_urlpatterns)),
    path('v1/', include(v1_router.urls)),
]
