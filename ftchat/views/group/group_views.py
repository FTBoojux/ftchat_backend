from ftchat.views.AuthenticateView import AuthenticateView
from ftchat.utils import jwt_util as jwt_utils
from ftchat.models import Group,GroupMember,Conversation,Participant
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