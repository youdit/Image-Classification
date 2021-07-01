import django_heroku

# default: use settings from main settings.py if not overwritten
from .settings import *


############
# SECURITY #
############

DEBUG = False

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)

ALLOWED_HOSTS = ['image-classification-densenet.herokuapp.com.herokuapp.com']

# Activate Django-Heroku.
django_heroku.settings(locals())