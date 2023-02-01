from django.urls import include, path
from rest_framework import routers

from api.views import CommentViewSet, SignUpView, ReviewViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    r'titles\/(?P<title_id>\d+)\/reviews', ReviewViewSet, basename='reviews',
)
router.register(
    r'titles\/(?P<title_id>\d+)\/reviews/(?P<review_id>\d+)\/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('auth/signup/', SignUpView.as_view()),
    path('', include(router.urls)),
]
