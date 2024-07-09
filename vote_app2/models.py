from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

import random
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, bypass_otp=False, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if bypass_otp:
            user.is_verified = True  # Assuming bypassing OTP means user is verified
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    # Add username field with a default value (e.g., empty string)
    username = models.CharField(max_length=150, unique=True, default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']  # List any additional required fields here

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()

    def verify_otp(self, otp, bypass_otp=False):
        if bypass_otp or self.otp == otp:
            self.otp = None
            self.is_verified = True
            self.save()
            return True
        return False

class Contestant(models.Model):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name
    

class Score(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.contestant.full_name} - Score: {self.score} - Time: {self.timestamp}"


class Assignment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)