import django_heroku

# default: use settings from main settings.py if not overwritten
from .settings import *


############
# SECURITY #
############

DEBUG = False

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', SECRET_KEY)

INSTALLED_APPS.append('whitenoise.runserver_nostatic')
MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_USE_FINDERS = True

ALLOWED_HOSTS = ['image-classification-densenet.herokuapp.com']



# Activate Django-Heroku.
django_heroku.settings(locals())