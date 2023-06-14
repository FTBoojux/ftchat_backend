from ftchat.views.AuthenticateView import AuthenticateView
from django.http import JsonResponse
from ftchat.models import GptConversation
from ftchat.utils import jwt_util as jwt_utils
from ftchat.service import gpt_conversation as gpt_conversation_service

class ConversationCreateView(AuthenticateView):
    def post(self,request,*args,**kwargs):
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        title = request.data.get('title')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        res = gpt_conversation_service.create_conversation(uid,title)
        return JsonResponse({'result':'success','message':'','code':200,'data':res})