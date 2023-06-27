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
    
class AddContactView(AuthenticateView):
    def post(self,request,*args,**kwargs):
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        target = request.data.get('target')
        message = request.data.get('message')
        res = account_service.add_contact(uid,target,message)
        return JsonResponse({'result':'success','message':'','code':200,'data':res})
    
class LogoutView(AuthenticateView):
    def post(self,request,*args,**kwargs):
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        token = jwt_utils.get_token_from_bearer(token)
        uid = jwt_utils.get_uid_from_jwt(token)
        res = account_service.logout(uid,token)
        return JsonResponse({'result':'success','message':'','code':200,'data':res})
    
class AvatarView(AuthenticateView):
    def get(self,request,*args,**kwargs):
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(request.META.get('HTTP_AUTHORIZATION')))
        res = account_service.get_avatar(uid)
        return JsonResponse({'result':'success','message':'','code':200,'data':res})
    
class UserInfoForEditView(AuthenticateView):
    def get(self,request,*args,**kwargs):
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(request.META.get('HTTP_AUTHORIZATION')))
        res = account_service.get_user_info(uid)
        return JsonResponse({'result':'success','message':'','code':200,'data':res})
    
    def post(self,request,*args,**kwargs):
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(request.META.get('HTTP_AUTHORIZATION')))
        username = request.data.get('username')
        bio = request.data.get('bio')
        avatar = request.data.get('avatar')
        sentiment_analysis_enabled = request.data.get('sentiment_analysis_enabled')
        res = account_service.update_user_info(uid,username,bio,avatar,sentiment_analysis_enabled)
        return JsonResponse({'result':'success','message':'','code':200,'data':res})