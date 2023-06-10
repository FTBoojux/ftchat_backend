from django.views import View
import ftchat.utils.jwt_util as jwt_utils
import ftchat.service.account as account_service
from django.http import JsonResponse
from ftchat.views.AuthenticateView import AuthenticateView

class UserInfoForAddView(AuthenticateView):
    def get(self,request,*args,**kwargs):
        keyword = request.GET.get('keyword')
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        users = account_service.search_contact(uid,keyword)
        return JsonResponse({'result':'success','message':'','code':200,'data':users})
    
class UserInfoForAddedView(AuthenticateView):
    def get(self,request,*args,**kwargs):
        keyword = request.GET.get('keyword')
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        users = account_service.search_stranger(uid,keyword)
        return JsonResponse({'result':'success','message':'','code':200,'data':users})