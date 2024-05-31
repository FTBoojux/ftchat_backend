from django.test import TestCase
import ftchat.service.attachment as attachment_service

class AttachmentTest(TestCase):
    def test_get_files_list(self):
        conversation_id = -1
        page_size = 10
        page_num = 1
        results = attachment_service.get_files_list(conversation_id, page_size, page_num)
        print(results)