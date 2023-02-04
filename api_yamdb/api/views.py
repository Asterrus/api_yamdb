from secrets import token_hex
from django.db.utils import IntegrityError
from api.filters import TitleFilter
from api.permissions import (IsAdminModeratorAuthorOrReadOnly, AdminOnly,
                             IsAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignUpSerializer, TitleReadSerializer,
                             TitleWriteSerializer, TokenSerializer,
                             UserSerializer, UserProfileSerializer)
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User


class SignUpView(APIView):
    """
    Отправить email с кодом подтверждения пользователю.
    Добавление пользователя в базу.'
    """
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            try:
                code = token_hex(16)
                user, created = User.objects.get_or_create(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email']
                )
                user.confirmation_code = code
                self.send_code(user.email, code)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response(
                    data={'error:': 'Username or Email already taken'},
                    status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_code(self, email, code):
        subject = 'YaMDB Confirmation Code'
        message = f'Confirmation Code: {code}'
        from_email = 'YaMDB@email.com'
        send_mail(subject, message, from_email, [email, ], fail_silently=False)


class TokenCreateView(APIView):
    """
    Отправить JWT токен пользователю.
    """
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = AccessToken.for_user(user)
            return Response({'token': str(token)})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    """
    Работа с моделью пользователей. Доступ: Админ.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminOnly, ]
    http_method_names = ['get', 'list', 'post', 'patch', 'delete', ]
    search_fields = ['username', ]
    lookup_field = 'username'


class UserProfileView(RetrieveUpdateAPIView):
    """
    Изменить данные пользователя. Доступ: Зарегистрированный пользователь.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user


class CategoryViewSet(CreateModelMixin, ListModelMixin,
                      DestroyModelMixin, GenericViewSet):
    """
    Получить список всех категорий. Доступ без токена
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(CreateModelMixin, ListModelMixin,
                   DestroyModelMixin, GenericViewSet):
    """
    Получить список всех жанров. Доступ без токена
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    """
    Получить список всех объектов. Права доступа: Доступно без токена
    """
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(ModelViewSet):
    """Представление отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly, )

    def get_queryset(self):
        """Получение всех отзывов к произведению."""
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()


class CommentViewSet(ModelViewSet):
    """Представление комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly, )

    def get_queryset(self):
        """Получение всех комментов к отзыву."""
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()
