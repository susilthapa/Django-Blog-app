from .base import *


SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG')

ALLOWED_HOSTS = ['meroblogpost.herokuapp.com']


STATIC_ROOT = os.path.join(BASE_DIR, 'live-static', 'static-root')  # for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'live-static', 'media-root')  # for production


import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)