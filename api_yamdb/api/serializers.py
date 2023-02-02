from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from yamdb.models import Category, Comment, Genre, Review, Title, User


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
    rating = serializers.IntegerField(read_only=True)

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
        if user:
            if user.confirmation_code == data['confirmation_code']:
                return data
            raise serializers.ValidationError('Wrong Code')
        raise serializers.ValidationError('User not exists')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)
