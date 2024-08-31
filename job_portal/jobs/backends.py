# backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

class NoPasswordBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            # Assuming we do not need to check password
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
