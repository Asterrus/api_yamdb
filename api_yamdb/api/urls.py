from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, SignUpView, TitleViewSet,
                       TokenCreateView, UserProfileView, UserViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'
router = DefaultRouter()
router.register('users', UserViewSet, basename='users'),
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'titles\/(?P<title_id>\d+)\/reviews', ReviewViewSet, basename='reviews',
)
router.register(
    r'titles\/(?P<title_id>\d+)\/reviews/(?P<review_id>\d+)\/comments',
    CommentViewSet,
    basename='comments',
)
urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenCreateView.as_view(), name='get_token'),
    path('v1/', include(router.urls)),
]
