from django.urls import path
from .views import LoginView, SignUpView


urlpatterns = [
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/signup/', SignUpView.as_view(), name="auth-register")
]