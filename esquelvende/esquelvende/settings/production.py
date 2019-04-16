import dj-database-url
from base import *

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
