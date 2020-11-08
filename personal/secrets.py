from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zfk+w9_u8*(lw%pgt6(k*-g0*=mcr7)-00k5q+30yf5y@goy@!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'news',
        'USER': 'postgres',
        'PASSWORD': 'Vaguita9000',
        'HOST': '127.0.0.1,',
        'PORT': '5432',
    }
}