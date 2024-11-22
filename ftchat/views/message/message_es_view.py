from django.http import JsonResponse
from ftchat.views.AuthenticateView import AuthenticateView
from ftchat.utils import jwt_util as jwt_utils
from ftchat.utils import elasticsearch_util as es_util
from ftchat.service import message as message_service

class MessageEsView(AuthenticateView):
    def get(self, request, conversation_id, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        keyword = request.GET.get('keyword')
        type = request.GET.get('type')
        pageNum = (int)(request.GET.get('pageNum'))
        pageSize = (int) (request.GET.get('pageSize'))
        res = es_util.conversation_message_search(conversation_id, keyword, pageNum, pageSize)
        return JsonResponse({'result': 'success', 'message': '', 'code': 200, 'data': res})