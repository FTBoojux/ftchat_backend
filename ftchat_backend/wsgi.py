"""
WSGI config for ftchat_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import threading
from ftchat import tasks as task
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ftchat_backend.settings')

threading.Thread(target=task.process_message).start()

application = get_wsgi_application()
