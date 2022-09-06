from rest_framework.routers import SimpleRouter
from django.urls import include, path
from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = SimpleRouter()

router.register('categories', CategoryViewSet, basename='category')
router.register('titles', TitleViewSet, basename='title')
router.register('genries', GenreViewSet, basename='genre')


urlpatterns = [
    path('', include(router.urls)),
]
