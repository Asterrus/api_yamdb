from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import viewsets
from rest_framework.filters import SearchFilter
# from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from yamdb.models import Category, Genre, Title

from .filters import TitleFilter
from .mixins import ModelMixinSet
from .permissions import IsAdminUserOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitleWriteSerializer)


class CategoryViewSet(ModelMixinSet):
    """
    Получить список всех категорий. Доступ без токена
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name', )
    lookup_field = 'slug'
    
    
class GenreViewSet(ModelMixinSet):
    """
    Получить список всех жанров. Доступ без токена
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """
    Получить список всех объектов. Права доступа: Доступно без токена
    """
    queryset = Title.objects.all()
    # queryset = Title.objects.annotate(
    #     rating=Avg('reviews__score')
    # ).all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer