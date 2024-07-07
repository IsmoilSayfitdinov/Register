from django.db import models
from users.models import UserModel
# Create your models here.
class BlogModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="blog")
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'
    
    