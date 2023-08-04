from ftchat.views.AuthenticateView import AuthenticateView
from ftchat.utils import jwt_util as jwt_utils
from ftchat.models import Group,GroupMember,Conversation,Participant,GroupJoinRequest
from ftchat.service import group as group_service
from django.http import JsonResponse

class GroupView(AuthenticateView):
    def post(self,request):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        group_name = request.data.get('name')
        group_avatar = request.data.get('avatar')
        announcement = request.data.get('announcement')
        # 创建群聊并返回群聊id
        group_id = Group.objects.create(
            group_name=group_name,
            avatar=group_avatar,
            announcement=announcement,
            owner=uid
        ).group_id
        GroupMember.objects.create(
            group=group_id,
            user=uid,
            role=1
        )
        conversation_id = Conversation.objects.create(
            type='G',
            group=group_id
        ).id
        Participant.objects.create(
            conversation=conversation_id,
            user=uid
        )
        
        return JsonResponse({'result':'success','message':'创建成功','code':200,'data':''})
    
class GroupJoinRequestView(AuthenticateView):
    def get(self,request):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        res = group_service.get_group_join_requests(uid)
        return JsonResponse({'result':'success','message':'','code':200,'data':res})
    def post(self,request,group_id):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        message = request.data.get('message')
        res = group_service.save_group_Join_request(uid,group_id,message)
        return res
    def put(self,request,group_id):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        operation = request.data.get('operation')
        requester = request.data.get('requester')
        res = {}
        if operation == 'reject':
            res = group_service.reject_group_join_request(uid,group_id,requester)
        elif operation == 'accept':
            res = group_service.accept_group_join_request(uid,group_id,requester)
        return res