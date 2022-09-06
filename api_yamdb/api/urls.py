from rest_framework.routers import SimpleRouter
from django.urls import include, path
from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = SimpleRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register('genries', GenreViewSet, basename='genries')


urlpatterns = [
    path('api/v1/', include(router.urls)),
]
