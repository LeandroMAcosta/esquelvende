from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL using email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email')
        try:
            user = UserModel._default_manager.get(email=username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if (user.check_password(password) and
                    self.user_can_authenticate(user)):
                return user
