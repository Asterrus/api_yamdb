from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message='this email is already taken')])
    username = serializers.RegexField(
        required=True, max_length=150, regex=r'^[\w.@+-]+$',
        validators=[UniqueValidator(queryset=User.objects.all(),
                                    message='this username is already taken')])

    class Meta:
        model = User
        fields = ['username', 'email', 'bio',
                  'first_name', 'last_name', 'role']


class UserProfileSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(
        required=True, max_length=150, regex=r'^[\w.@+-]+$')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('me - not allowed username')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        required=True, max_length=150, regex=r'^[\w.@+-]+$')
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        data['user'] = user
        if user.confirmation_code == data['confirmation_code']:
            return data
        raise serializers.ValidationError('Wrong Code')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        lookup_field = 'slug'
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        lookup_field = 'slug'
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.DecimalField(
        read_only=True, max_digits=3, decimal_places=2)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('title',)

    def create(self, validated_data):
        title_id = self.context.get('view').kwargs.get('title_id')
        author = self.context['request'].user
        validated_data['title'] = Title.objects.get(pk=title_id)
        validated_data['author'] = author
        return super(ReviewSerializer, self).create(validated_data)
    

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)
