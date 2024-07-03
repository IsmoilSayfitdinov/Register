from .views import UserRegistrationViewSet, VerifyCodeView, LoginView, UpdateUserView
from django.urls import path

urlpatterns = [
    path('register/', UserRegistrationViewSet.as_view()),
    path('verify/', VerifyCodeView.as_view()),
    path('login/', LoginView.as_view()),
    path('update/', UpdateUserView.as_view()),
]