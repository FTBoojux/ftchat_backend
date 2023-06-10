from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from rest_framework import exceptions
from ftchat.utils import jwt_util as jwt_utils
from ftchat.models import User
        
class MyCustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        if uid is None:
            raise exceptions.AuthenticationFailed('用户未登录')
        user = User.objects.get(user_id=uid)
        if user is None:
            raise exceptions.AuthenticationFailed('用户不存在')
        return (user,token)
    
class AuthenticateView(APIView):
    authentication_classes = (MyCustomAuthentication,)
    permission_classes = (IsAuthenticated,)