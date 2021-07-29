# coding: utf-8

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.decorators import api_view

from app_user.models import User
from core.response import response_ok


class UserView(APIView):
    """用户信息"""

    def get(self, request: Request) -> JsonResponse:
        user_id = request.query_params.get('userId')
        obj = User.objects.get(user_id=user_id)
        return

    def post(self, request):
        return


@api_view()
def test(request: Request):
    print(type(request))
    print(request.ext)
    return response_ok()
