from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from yamdb.models import Category, Genre, Title

from .filters import TitleFilter
from .mixins import ModelMixinSet
from .permissions import IsAdminUserOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitleWriteSerializer)

from secrets import token_hex

from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from yamdb.models import User
from api.serializers import SignUpSerializerб TokenSerializer


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


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass

