from django.contrib.auth.backends import ModelBackend

from .models import UserInfo


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(email=username)
        except UserInfo.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user


class NicknameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(nick_name=username)
        except UserInfo.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
