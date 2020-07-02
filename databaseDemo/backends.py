from USER.models import UserInfo


class EmailBackend(object):
    def authenticate(self, request, **credentials):
        email = credentials.get('email', credentials.get('username'))
        try:
            user = UserInfo.objects.get(email=email)
        except UserInfo.DoesNotExist:
            pass
        else:
            if user.check_password(credentials["password"]):
                return user

    def get_user(self, user_id):
        try:
            return UserInfo.objects.get(index=user_id)
        except UserInfo.DoesNotExist:
            return None


class NicknameBackend(object):
    def authenticate(self, request, **credentials):
        nick_name = credentials.get('nick_name', credentials.get('username'))
        try:
            user = UserInfo.objects.get(nick_name=nick_name)
        except UserInfo.DoesNotExist:
            pass
        else:
            if user.check_password(credentials["password"]):
                return user

    def get_user(self, user_id):
        try:
            return UserInfo.objects.get(index=user_id)
        except UserInfo.DoesNotExist:
            return None
