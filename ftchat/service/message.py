from ftchat.models import ContactRequest

def get_message_nums(uid):
    contacts = ContactRequest.objects.filter(receiver=uid,status="pending").count()
    return {"contacts":contacts,"messages":0}