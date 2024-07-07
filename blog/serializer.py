from rest_framework import serializers
from users.models import UserModel
from .models import BlogModel
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username']

class BlogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = BlogModel
        fields = ['id', 'image', 'title', 'content', "user"]
