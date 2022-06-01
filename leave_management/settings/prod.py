from .common import *

# Nginx가 프록시 서버 역할을 하고있고, http://127.0.0.1:8000으로 리디렉션 하고있기에,
# 허용 API를 127.0.0.1로 설정함.
ALLOWED_HOSTS = ["127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["https://*.joje.link"]  # 안전하지 않은 요청에 대한 신뢰할 수 있는 출처 목록 (CSRF 오류로 인해 설정)
DEBUG = False

STATIC_ROOT = os.getenv("STATIC_ROOT")  # 배포서버에서 입력받음 (/var/www/staticfiles)

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
