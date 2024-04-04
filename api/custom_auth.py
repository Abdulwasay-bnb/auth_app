from rest_framework.authentication import BaseAuthentication
from members.models import CustomUser
from rest_framework.exceptions import AuthenticationFailed

class custom_auth(BaseAuthentication):
    def authenticate(self,request):
        email = request.GET.get('email')
        if email is None:
            return None
        try:
            user = CustomUser.object.get(email=email)
        except:
            raise AuthenticationFailed('No such email or password exit')
        return (user,None)