from django.http import JsonResponse
from ftchat.views.AuthenticateView import AuthenticateView
from ftchat.utils import jwt_util as jwt_utils
from ftchat.service import message as message_service


class MessageNums(AuthenticateView):
    def get(self,request,*args,**kwargs):
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        res = message_service.get_message_nums(uid)
        return JsonResponse({'result':'success','message':'','code':200,'data':res})