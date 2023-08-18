from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog_app.models import NULLABLE, Product


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='e-mail')

    avatar = models.ImageField(upload_to='user/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    country = models.CharField(max_length=150, verbose_name='страна', **NULLABLE)

    email_verified = models.BooleanField(default=False, verbose_name='Почта подтверждена')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
