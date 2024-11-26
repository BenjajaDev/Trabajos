"""
Configuraciones de Django para el proyecto sistema.

Generado por 'django-admin startproject' utilizando Django 5.0.1.

Para más información sobre este archivo, consulta
https://docs.djangoproject.com/en/5.0/topics/settings/

Para la lista completa de configuraciones y sus valores, consulta
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from mongoengine import connect

#construye rutas dentro del proyecto de esta manera: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / 'templates'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
SECRET_KEY = 'django-insecure-#kex!27sc#d2razc=i+gx7p77-f5e4=&_z)vrm*gvm#-+fmnzn'
DEBUG = True

ALLOWED_HOSTS = [] #lista de hosts permitidos


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin', #aplicación del panel de administración
    'django.contrib.auth',  #aplicación de autenticación
    'django.contrib.contenttypes',  #aplicación para tipos de contenido
    'django.contrib.sessions',  #aplicación para manejo de sesiones
    'django.contrib.messages',  #aplicación para mensajes
    'django.contrib.staticfiles',  #aplicación para archivos estáticos
    'sistemaApp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',#middleware de seguridad
    'django.contrib.sessions.middleware.SessionMiddleware',  #middleware de sesiones
    'django.middleware.common.CommonMiddleware',  #middleware común
    'django.middleware.csrf.CsrfViewMiddleware',  #middleware de protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  #middleware de autenticación
    'django.contrib.messages.middleware.MessageMiddleware',  #middleware para mensajes
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  #middleware para prevenir clickjacking
]
#archivo de configuración de URLs
ROOT_URLCONF = 'sistema.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], #backend de templates de Django
        'APP_DIRS': True, #permitir búsqueda de templates en directorios de aplicaciones
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sistema.wsgi.application'



# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
#configuración de MongoDB
MONGODB_SETTINGS = {
    'DB': 'sistema', #nombre de la base de datos
    'HOST': 'localhost',
    'PORT': 27017,
}
#conexión a MongoDB
connect(
    db=MONGODB_SETTINGS['DB'],
    host=MONGODB_SETTINGS['HOST'],
    port=MONGODB_SETTINGS['PORT'],
    )

#configuración de bases de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIFILES_DIRS = [STATIC_URL]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
