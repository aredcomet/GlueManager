from .common import *  # noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DJANGO_DB_NAME', default='glue_manager'),
        'HOST': env('DJANGO_DB_HOST', default='database'),
        'USER': env('DJANGO_DB_USER', default='postgres'),
        'PORT': env('DJANGO_DB_PORT', default='5432'),
        'PASSWORD': env('DJANGO_DB_PASSWORD', default='postgres'),
        'ATOMIC_REQUESTS': True,
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

TIME_ZONE = 'Asia/Kolkata'
