import os
from pathlib import Path
from decouple import config, Csv
from dj_database_url import parse as dburl

# Caminhos do projeto
BASE_DIR = Path(__file__).resolve().parent.parent  # Corrigido para usar pathlib
PROJECT_ROOT = BASE_DIR.parent

# Configurações básicas
SECRET_KEY = config('SECRET_KEY', default='uma-chave-secreta-segura')
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts permitidos
ALLOWED_HOSTS = ['nformasmoveis.com.br', 'www.nformasmoveis.com.br', '127.0.0.1', 'localhost', '0.0.0.0']

# Configuração do banco de dados
DEFAULT_DATABASE_URL = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Agora funciona corretamente
    }
}

# Aplicativos instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Ferramentas de desenvolvimento
    'django_extensions',
    'pandas',

    # Aplicativos personalizados
    'erp_mpro.apps.base',
    'erp_mpro.apps.login',
    'erp_mpro.apps.cadastro',
    'erp_mpro.apps.vendas',
    'erp_mpro.apps.compras',
    'erp_mpro.apps.fiscal',
    'erp_mpro.apps.financeiro',
    'erp_mpro.apps.estoque',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middleware personalizado para login obrigatório
    'erp_mpro.middleware.LoginRequiredMiddleware',
]

# Configuração de URLs
ROOT_URLCONF = 'erp_mpro.urls'

# Configuração de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Contextos personalizados
                'erp_mpro.apps.base.context_version.sige_version',
                'erp_mpro.apps.login.context_user.foto_usuario',
            ],
        },
    },
]

# Configuração do WSGI
WSGI_APPLICATION = 'erp_mpro.wsgi.application'

# Validação de senha
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

# Internacionalização e fuso horário
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Diretório de arquivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Diretório de arquivos de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Diretório para fixtures
FIXTURE_DIRS = [BASE_DIR / 'fixtures']

# Configurações de sessão
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
LOGIN_NOT_REQUIRED = (
    r'^/login/$',
    r'^/login/esqueceu/$',
    r'^/login/trocarsenha/$',
    r'^/logout/$',
)

# Configurações de e-mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='seu-email@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='sua-senha-secreta')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='webmaster@exemplo.com')

# Configuração de logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Configuração de CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://nformasmoveis.com.br',
    'https://www.nformasmoveis.com.br'
]

