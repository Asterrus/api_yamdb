from django.urls import path

from .views import SignUpView, TokenCreateView

urlpatterns = [
    path('auth/signup/', SignUpView.as_view()),
    path('auth/token/', TokenCreateView.as_view()),
]
