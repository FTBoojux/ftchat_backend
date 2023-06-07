import json

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ftchat.utils.openai_util import send_to_gpt

model_table = {
    'gpt-4': 'gpt-4',
    'gpt-3.5-turbo': 'gpt-3.5-turbo'
 }

@require_POST
@csrf_exempt
def chat_to_gpt(request):
    data = json.load(request)
    model_choosed = data.get('model', 'gpt-3.5-turbo')
    model = model_table.get(model_choosed, 'gpt-3.5-turbo')
    msg = data.get('message', '')
    if not msg:
        return JsonResponse({'result': 'error', 'message': 'msg is required', 'code': 200})
    try:
        result = send_to_gpt(msg, model)
        # 取result['choices'][0]['message']['content']的值
        result_content = result['choices'][0]['message']['content']
        print(result_content)
        return JsonResponse({'result': 'success', 'message': result_content, 'code': 200})
    except Exception as e:
        # 控制台打印错误
        print(e)
        return JsonResponse({'result': 'error', 'message': '发送失败，请重试', 'code': 200})