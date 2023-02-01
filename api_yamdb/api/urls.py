from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
# router.register('titles', TitleViewSet)
# router.register('genres', GenresViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 
