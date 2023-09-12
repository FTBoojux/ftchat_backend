from ftchat.views.AuthenticateView import AuthenticateView
import ftchat.utils.jwt_util as jwt_utils
import ftchat.service.group as group_service
from django.http import JsonResponse
from rest_framework import exceptions

class GroupMembersView(AuthenticateView):
    def get(self,request,conversation_id):
        mode = request.META.get('HTTP_MODE')
        uid = ""
        if mode == 'outer':
            token = request.META.get('HTTP_AUTHORIZATION')
            uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        elif mode == 'inner':
            token = request.META.get('HTTP_AUTHORIZATION')
            uid = jwt_utils.get_uid_from_jwt_inner(token)
        else:
            raise exceptions.AuthenticationFailed('未知的请求来源')    
        res = group_service.get_group_members(conversation_id,mode == 'outer', uid)
        return res
    def post(self,request,group_id):
        pass
    def delete(self,request,group_id):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        res = group_service.delete_group_member(uid,group_id)
        return res
    def put(self,request,group_id):
        pass