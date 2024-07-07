from django.db import models
import random

class User(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)  # Thêm trường này

    def __str__(self):
        return self.email

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()

    def verify_otp(self, otp):
        if self.otp == otp:
            self.otp = None
            self.is_verified = True
            self.save()
            return True
        return False
