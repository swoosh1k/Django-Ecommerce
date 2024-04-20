import os
from pathlib import Path
abc = 'csa'


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False


ALLOWED_HOSTS = ['127.0.0.1']

SECRET_KEY = 'django-insecu2efsde32442df-=5vw=rdvsqg%3**g8&rt3z@=-01e-yy=5f5r)$g4%%zlg(7rxy'

DATABASES = {
   'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': 'laminart',
      'USER': 'userdb',
      'PASSWORD': '123456',
      'HOST': 'localhost',
      'PORT': '5432',
   }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
   os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')