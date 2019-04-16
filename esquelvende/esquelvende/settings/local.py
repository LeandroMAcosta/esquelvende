from base import *

SECRET_KEY = 'i4nb&02v%0_pb+9931ci-z@bjo1t!$u0072zt55hk0j#3+)7(2'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'esquelvende',
        'USER': 'admin',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'PORT': '',
        'CHARSET': 'UTF8',
    }
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1063990601253-4vci3d73c2mqrmln4d14h5aqsalpt8em.apps.googleusercontent.com'  #Paste CLient Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'U7Hd9MKp3L7DeyqvJYEhg26F'
SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True

SOCIAL_AUTH_FACEBOOK_KEY = '548109182040282'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '372116829fb504573670f7f55013e962'  # App Secret
