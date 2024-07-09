from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
import random

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
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)
    username = models.CharField(max_length=150, unique=True, default='')
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

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

class ContestantManager(BaseUserManager):
    def create_contestant(self, email, password=None,bypass_otp=False, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        contestant = self.model(email=email, **extra_fields)
        contestant.set_password(password)
        if bypass_otp:
            contestant.is_verified = True  # Assuming bypassing OTP means user is verified
        contestant.save(using=self._db)
        return contestant

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_contestant(email, password, **extra_fields)

class Contestant(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    is_verified = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name='contestant_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='contestant_set', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'date_of_birth']

    objects = ContestantManager()

    def __str__(self):
        return self.email

# Define related_name for Score and Assignment models
class Score(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='scores')
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE, related_name='scores')
    score = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.contestant.full_name} - Score: {self.score} - Time: {self.timestamp}"

class Assignment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assignments')
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE, related_name='assignments')
