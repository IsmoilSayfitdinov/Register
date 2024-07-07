from django.urls import path
from .views import BlogsCreate, BlogList, BlogeUpdate, BlogDelete, BlogDeatail, MySelfBlog

urlpatterns = [
    path('create/', BlogsCreate.as_view()),
    path('list/', BlogList.as_view()),
    path('<int:pk>/update/', BlogeUpdate.as_view()),
    path('<int:pk>/delete/', BlogDelete.as_view()),
    path('<int:pk>/', BlogDeatail.as_view()),
    path('myblog/', MySelfBlog.as_view()),
]