from .common import *

"""
참고
- collectstatic을 실행하기 위해서 배포 서버(ubuntu)에 ~/Projects/에 leave_management 프로젝트가 풀 되어있다.
- ubuntu에서 poetry와 다른 패키지(postgresql 등)간의 충돌이 꾸준히 있어서, 기본 파이썬 환경에 django만 설치한 env환경을 별도로 구성했다.
- 최대한 다른 설정과의 의존성을 피하기 위해 collectstatic을 위한 설정 파일을 별도로 분리하였다. (실행은 git action 참고)
"""

STATIC_ROOT = "/var/www/staticfiles"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'members',
]