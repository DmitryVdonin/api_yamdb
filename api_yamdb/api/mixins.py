from rest_framework import mixins, viewsets


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Дает возможность на чтение всех объектов,
    добавление и удаление объекта.
    """
    pass
