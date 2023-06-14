from ftchat.models import GptConversation

def create_conversation(user_id, title):
    conversation = GptConversation.objects.create(
        user_id=user_id,
        title=title
    )
    return conversation.conversation_id