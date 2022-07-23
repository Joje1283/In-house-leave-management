import sys
from .common import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Nginx가 프록시 서버 역할을 하고있고, http://127.0.0.1:8000으로 리디렉션 하고있기에,
# 허용 API를 127.0.0.1로 설정함.
ALLOWED_HOSTS = ["127.0.0.1"]
ALLOWED_HOSTS += [os.getenv("ALLOWED_HOST")]
CSRF_TRUSTED_ORIGINS = ["https://*.joje.link"]  # 안전하지 않은 요청에 대한 신뢰할 수 있는 출처 목록 (CSRF 오류로 인해 설정)
DEBUG = False

STATIC_ROOT = os.getenv("STATIC_ROOT")  # 배포서버에서 입력받음 (/var/www/staticfiles)

if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'leave',
            'USER': os.getenv("DB_USER"),
            'PASSWORD': os.getenv("DB_PASSWORD"),
            'HOST': os.getenv("DB_HOST"),
            'PORT': os.getenv("DB_PORT"),
        }
    }


# sentry 설정
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# rabbitMQ
# sudo docker run -d --name rabbitmq -p {{your_port}}:{{your_port}} -p {{your_web_port}}:{{your_web_port}} --restart=unless-stopped -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS={{your password}} rabbitmq:management
