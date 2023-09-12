from ftchat.views.AuthenticateView import AuthenticateView
import ftchat.utils.jwt_util as jwt_utils
import ftchat.service.group as group_service
from django.http import JsonResponse

class GroupMembersView(AuthenticateView):
    def get(self,request,group_id):
        res = group_service.get_group_members(group_id)
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