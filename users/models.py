from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser, PermissionsMixin
import uuid
import random
class UserModel(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    verify_code = models.CharField(max_length=4)
    
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['password']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username

    def password_check(self):
        if not self.password:
            self.password = str(uuid.uuid4())

    def hashing_password(self):
        if not self.password.startswith("pbkdf2_sha256"):
            self.set_password(self.password)

    def create_verify_code(self):
        code = str(random.randint(1000, 9999))
        self.verify_code = code
        VerifyCodeModel.objects.create(
            code=code,
            user=self
        ).save()
        return code
            
            
class VerifyCodeModel(models.Model):
    code = models.CharField(max_length=4)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.code
    
    
    def save(self, *args, **kwargs):
        super(VerifyCodeModel, self).save(*args, **kwargs)