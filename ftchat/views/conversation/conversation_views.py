import json
from ftchat.views.AuthenticateView import AuthenticateView
from ftchat.service import conversation as conversation_service
from ftchat.utils import jwt_util as jwt_utils
from django.http import JsonResponse
import base64

class ConversationView(AuthenticateView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        conversation = conversation_service.get_conversations(uid)
        return JsonResponse({'result':'success','message':'','code':200,'data':conversation})
    
class ConversationMessageView(AuthenticateView):
    def get(self, request, conversation_id):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        paging_state = request.GET.get('paging_state')
        page_size = request.GET.get('page_size',10)
        if paging_state is not None:
            paging_state = base64.b64decode(paging_state)
        page_size = int(page_size)
        return conversation_service.get_message_list(uid,conversation_id, page_size,paging_state)
    def post(self, request, conversation_id):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        message = request.data.get('message')
        _type = request.data.get('type')
        # message不是字符串的话，转换成 json 字符串
        if type(message) != str:
            message = json.dumps(message)
        res = conversation_service.save_message(uid,conversation_id,message,_type)
        return res
    def delete(self, request, conversation_id):
        pass
    def put(self, request, conversation_id):
        pass    