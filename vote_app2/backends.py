from django.contrib.auth.backends import BaseBackend
from .models import CustomUser, Contestant

class CustomUserBackend(BaseBackend):

    def authenticate(self, request=None, email=None, password=None):
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

class ContestantBackend(BaseBackend):
    def authenticate(self, request=None, email=None, password=None):
        try:
            contestant = Contestant.objects.get(email=email)
            if contestant.check_password(password):
                return contestant
        except Contestant.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Contestant.objects.get(pk=user_id)
        except Contestant.DoesNotExist:
            return None