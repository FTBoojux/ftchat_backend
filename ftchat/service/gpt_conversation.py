from ftchat.models import GptConversation
from django.forms.models import model_to_dict

def create_conversation(user_id, title):
    conversation = GptConversation.objects.create(
        user_id=user_id,
        title=title
    )
    return conversation.conversation_id

def get_conversation_list(user_id):
    conversation_qs = GptConversation.objects.filter(user_id=user_id)
    conversation_list = [model_to_dict(conversation) for conversation in conversation_qs]
    return conversation_list

def delete_conversation(user_id, conversation_id):
    conversation = GptConversation.objects.get(conversation_id=conversation_id)
    if conversation.user_id == user_id:
        conversation.delete()
        return True
    else:
        return False