from ftchat.views.AuthenticateView import AuthenticateView
from ftchat.service import conversation as conversation_service
from ftchat.utils import jwt_util as jwt_utils

from django.http import JsonResponse

class ConversationView(AuthenticateView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        conversation = conversation_service.get_conversations(uid)
        return JsonResponse({'result':'success','message':'','code':200,'data':conversation})
    
class ConversationMessageView(AuthenticateView):
    def get(self, request, conversation_id):
        pass
    def post(self, request, conversation_id):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        message = request.data.get('message')
        res = conversation_service.save_message(uid,conversation_id,message)
        return res
    def delete(self, request, conversation_id):
        pass
    def put(self, request, conversation_id):
        pass    