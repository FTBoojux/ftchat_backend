from ftchat.views.AuthenticateView import AuthenticateView
from django.http import JsonResponse
import base64

from ftchat.utils import jwt_util as jwt_utils
from ftchat.service import gpt_conversation as gpt_conversation_service
import ftchat.utils.openai_util as openai_util
import ftchat.utils.cassandra_util as cassandra_util
model_table = {
    'gpt-4': 'gpt-4',
    'gpt-3.5-turbo': 'gpt-3.5-turbo'
 }

class ConversationView(AuthenticateView):
    def post(self,request,*args,**kwargs):
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        title = request.data.get('title')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        res = gpt_conversation_service.create_conversation(uid,title)
        return JsonResponse({'result':'success','message':'','code':200,'data':res})
    
    def get(self,request,*args,**kwargs):
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        res = gpt_conversation_service.get_conversation_list(uid)
        return JsonResponse({'result':'success','message':'','code':200,'data':res})
    
    def delete(self,request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        conversation_id = request.data.get('conversation_id')
        res = gpt_conversation_service.delete_conversation(uid,conversation_id)
        return JsonResponse({'result':'success','message':'','code':200,'data':res})
    
class GptConversation(AuthenticateView):
    def post(self,request,*args,**kwargs):
        # 获取header中的token
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        model_choosed = request.data.get('model', 'gpt-3.5-turbo')
        # model_choosed = data.get('model', 'gpt-3.5-turbo')
        model = model_table.get(model_choosed, 'gpt-3.5-turbo')
        msg = request.data.get('message', '')
        conversation_id = request.data.get('conversation_id')
        cid_str = str(conversation_id)
        cassandra_util.save_message(content=msg,sender=uid,receiver='1',conversation_id=cid_str)
        if not msg:
            return JsonResponse({'result': 'error', 'message': 'msg is required', 'code': 200})
        try:
            result = openai_util.send_to_gpt(msg, model)
            # 取result['choices'][0]['message']['content']的值
            result_content = result['choices'][0]['message']['content']
            print(result_content)
            cassandra_util.save_message(content=result_content,sender='1',receiver=uid,conversation_id=cid_str)
            return JsonResponse({'result': 'success', 'message': result_content, 'code': 200})
        except Exception as e:
            # 控制台打印错误
            print(e)
            cassandra_util.save_message(content=str(e),sender='1',receiver=uid,conversation_id=cid_str)
            return JsonResponse({'result': 'error', 'message': '发送失败，请重试', 'code': 200})
        
    def get(self,request,*args,**kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        uid = jwt_utils.get_uid_from_jwt(jwt_utils.get_token_from_bearer(token))
        conversation_id = request.GET.get('conversation_id')
        paging_state = request.GET.get('paging_state')
        if paging_state is not None:
            paging_state = base64.b64decode(paging_state)

        rows, next_paging_state = cassandra_util.get_message_list(uid, '1', str(conversation_id), paging_state=paging_state)

        if next_paging_state is not None:
            next_paging_state = base64.b64encode(next_paging_state).decode()
        result = [{'role':'bot' if row.sender == '1' else 'user','content':row.content} for row in rows][::-1]
        return JsonResponse({'result':'success','message':'','code':200,'data':result, 'next_paging_state': next_paging_state})