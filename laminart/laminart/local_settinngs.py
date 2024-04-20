import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-=5vw=rdvsqg%3**g8&rt3z@=-01e-yy=5f5r)$g4%%zlg(7rxy'

DEBUG = True

ALLOWED_HOSTS = []



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
   os.path.join(BASE_DIR, "static"),
]



TELEGRAM_BOT_TOKEN = '7127890351:AAFEWmzyAr4CJODSuFvwGJ57ZTQHqutoYJg'
TELEGRAM_BOT_CHAT_ID = '545589900'