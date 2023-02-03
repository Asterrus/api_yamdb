from secrets import token_hex

from api.filters import TitleFilter
from api.mixins import ModelMixinSet
from api.permissions import (AdminModeratorAuthorPermission, AdminOnly,
                             IsAdminUserOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignUpSerializer, TitleReadSerializer,
                             TitleWriteSerializer, TokenSerializer,
                             UserSerializer, UserProfileSerializer)
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.tokens import AccessToken
from yamdb.models import Category, Genre, Review, Title, User


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            code = token_hex(16)
            self.send_code(email, code)
            # Громоздко выглядит, потом поправлю.
            if not User.objects.filter(username=username, email=email).exists():
                if (User.objects.filter(username=username).exists()
                        or User.objects.filter(email=email).exists()):
                    message = 'Username or Email already taken'
                    return Response(
                        data={'error:': message},
                        status=status.HTTP_400_BAD_REQUEST)
                User.objects.create(
                    email=email, username=username, confirmation_code=code)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_code(self, email, code):
        subject = 'YaMDB Confirmation Code'
        message = f'Confirmation Code: {code}'
        from_email = 'YaMDB@email.com'
        send_mail(subject, message, from_email, [email, ], fail_silently=False)


class TokenCreateView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = User.objects.filter(username=username).first()
            token = AccessToken.for_user(user)
            return Response({'token': str(token)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminOnly, ]
    http_method_names = ['get', 'list', 'post', 'patch', 'delete', ]
    filter_backends = [SearchFilter, ]
    search_fields = ['username', ]
    lookup_field = 'username'


class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user

class CategoryViewSet(ModelMixinSet):
    """
    Получить список всех категорий. Доступ без токена
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
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
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (AdminModeratorAuthorPermission,)
    pagination_class = LimitOffsetPagination

    def get_title(self):
        """Получение произведения."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        """Получение всех отзывов к произведению."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создание отзыва авторизованнным пользователем."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Представление комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (AdminModeratorAuthorPermission,)

    def get_review(self):
        """Получение отзыва"""
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Получение всех комментов к отзыву."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создание коммента авторизованнным пользователем."""
        serializer.save(author=self.request.user, review=self.get_review())
