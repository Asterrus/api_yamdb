from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from yamdb.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')

# class GenreSerializer(serializers.ModelSerializer):
#     """Сериалайзер для модели Genre."""

#     class Meta:
#         model = Genre
#         fields = ('name', 'slug')
        
# class TitleReadSerializer(serializers.ModelSerializer):
#     """Сериалайзер для модели Title (чтение)."""

#     category = CategorySerializer(read_only=True)
#     genre = GenreSerializer(read_only=True, many=True)
#     rating = serializers.IntegerField(
#         source='reviews__score__avg', read_only=True, default=0
#     )

#     class Meta:
#         fields = (
#             'id',
#             'name',
#             'year',
#             'rating',
#             'description',
#             'genre',
#             'category',
#         )
#         model = Title