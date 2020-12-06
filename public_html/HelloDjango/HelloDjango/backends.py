from allauth.account.auth_backends import AuthenticationBackend

class AllowAllUsersModelBackend(AuthenticationBackend):

    def user_can_authenticate(self, user):
        return True