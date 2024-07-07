from .views import UserRegistrationViewSet, VerifyCodeView, LoginView, UpdateUserView, UdateUserForAdmin, DeleteUserForAdmin, UserListForAdmin
from django.urls import path

urlpatterns = [
    path('register/', UserRegistrationViewSet.as_view()),
    path('verify/', VerifyCodeView.as_view()),
    path('login/', LoginView.as_view()),
    path('update/', UpdateUserView.as_view()),
    
    path("list/", UserListForAdmin.as_view()),
    path("<int:pk>/update", UdateUserForAdmin.as_view()),
    path("<int:pk>/delete", DeleteUserForAdmin.as_view()),
]