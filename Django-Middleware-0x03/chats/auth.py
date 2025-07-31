from rest_framework import authentication


class UserAuthenticated(authentication.TokenAuthentication):

    def authenticate(self, request):
        return super().authenticate(request)