import json
from datetime import timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .tasks import send_welcome_email


@csrf_exempt
def debug(request):
    # 웰컴 이메일 테스트를 위한 API
    try:
        data = json.loads(request.body)
        send_welcome_email.apply_async([data.get("username")], eta=timezone.now() + timedelta(seconds=10), queue="paul_worker")
        return JsonResponse(data={"result": True})
    except Exception as e:
        print(e)
    return JsonResponse(data={"result": False})
