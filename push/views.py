from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from members.models import Member
import json


@csrf_exempt
def debug(request):
    # 웰컴 이메일 테스트를 위한 API
    try:
        data = json.loads(request.body)
        member = Member.objects.get(username=data.get("username"))
        member.send_welcome_email()
        return JsonResponse(data={"result": True})
    except Exception as e:
        print(e)
    return JsonResponse(data={"result": False})
