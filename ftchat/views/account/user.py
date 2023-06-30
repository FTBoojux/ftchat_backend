from django.views import View
import ftchat.utils.jwt_util as jwt_utils
import ftchat.service.account as account_service
from django.http import JsonResponse
from ftchat.views.AuthenticateView import AuthenticateView
from ftchat.models import User
from ftchat.utils.redis_utils import redis_client

class ContactView(AuthenticateView):
    def get(self,request,*args,**kwargs):
        keyword = request.GET.get('keyword')
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        users = account_service.search_contact(uid,keyword)
        return JsonResponse({'result':'success','message':'','code':200,'data':users})
    def post(self,request,*args,**kwargs):
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        contact_id = request.data.get('target')
        account_service.add_contact(uid,contact_id)
        return JsonResponse({'result':'success','message':'添加成功！','code':200,'data':''})
    def delete(self,request,user_id):
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        account_service.delete_contact(uid,user_id)
        return JsonResponse({'result':'success','message':'删除成功！','code':200,'data':''})

    
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
        redis_key = f"cadd:{uid}{target}"
        cadd = redis_client.get(redis_key)
        if cadd is not None:
            return JsonResponse({'result':'success','message':'','code':200,'data':{'res':False,'msg':'请勿频繁重复添加!'}})
        else:
            # 过期时间一天
            redis_client.set(redis_key,1,86400)
            message = request.data.get('message')
            res,msg = account_service.save_contact_request(uid,target,message)
            return JsonResponse({'result':'success','message':'','code':200,'data':{'res':res,'msg':msg}})
    def get(self,request,*args,**kwargs):
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        res = account_service.get_contact_requests(uid)
        for user in res:
            requester = User.objects.get(user_id=user['requester'])
            user['username'] = requester.username
            user['avatar'] = requester.avatar
        return JsonResponse({'result':'success','message':'','code':200,'data':res})
    def delete(self,request,*args,**kwargs):
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        target = request.data.get('target')
        account_service.reject_contact_request(uid,target)
        return JsonResponse({'result':'success','message':'已拒绝！','code':200,'data':''})

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