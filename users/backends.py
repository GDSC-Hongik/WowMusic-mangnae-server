# users/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 이메일을 username으로 사용하여 인증
            user = get_user_model().objects.get(email=username)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None
        return None
