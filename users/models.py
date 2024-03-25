from django.contrib.auth.models import AbstractUser
from django.db import models
from distribution.models import NULLABLE


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='Имейл')
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    phone = models.CharField(max_length=25, verbose_name='Телефон', **NULLABLE)
    telegram = models.CharField(max_length=150, verbose_name='Телеграм', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    email_confirmed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
