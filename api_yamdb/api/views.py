from api.serializers import CategorySerializer
from rest_framework import viewsets
from yamdb.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name', )
    lookup_field = 'slug'