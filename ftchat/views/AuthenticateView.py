from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from rest_framework import exceptions
from ftchat.utils import jwt_util as jwt_utils
from ftchat.models import User
        
class MyCustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        mode = request.META.get('HTTP_MODE')
        token = request.META.get('HTTP_AUTHORIZATION')
        if mode == 'outer' :
            uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))    
        elif mode == 'inner':
            uid = jwt_utils.get_uid_from_jwt_inner(token)
        if uid is None:
            raise exceptions.AuthenticationFailed('用户未登录')
        user = User.objects.get(user_id=uid)
        if user is None:
            raise exceptions.AuthenticationFailed('用户不存在')
        return (user,token)    
    
class InnerAuthenticateView(authentication.BaseAuthentication):
    def authenticate(self, request):
        mode = request.META.get('HTTP_MODE')
        token = request.META.get('HTTP_AUTHORIZATION')
        if mode == 'inner' :
            uid = jwt_utils.get_uid_from_jwt_inner(token)
        if uid is None:
            raise exceptions.AuthenticationFailed('用户未登录')
        user = User.objects.get(user_id=uid)
        if user is None:
            raise exceptions.AuthenticationFailed('用户不存在')
        return (user,token)

class AuthenticateView(APIView):
    authentication_classes = (MyCustomAuthentication,)
    permission_classes = (IsAuthenticated,)

class InnerAuthenticateView(APIView):
    authentication_classes = (InnerAuthenticateView,)
    permission_classes = (IsAuthenticated,)