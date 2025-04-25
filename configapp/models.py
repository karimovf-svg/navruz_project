from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
import re

class CustomUserManage(BaseUserManager):
    def normalize_phone_number(self, phone_number):
        normalized_phone = re.sub(r'\D', '', phone_number)
        return normalized_phone
    def create_user(self, phone_number, name=None, email=None, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone maydoni majburiy")
        phone_number = self.normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, password, email=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError("Superuser is_admin=True bo'lishi kerak")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser is_staff=True bo'lishi kerak")

        return self.create_user(phone_number, name, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=22)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    objects = CustomUserManage()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.phone_number

    @property
    def is_superuser(self):
        return self.is_admin


class ContactMessage(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    @property
    def has_replies(self):
        return self.replies.exists()

class MessageReply(models.Model):
    message = models.ForeignKey(ContactMessage, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    replied_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.message.subject}"