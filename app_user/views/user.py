# coding: utf-8

from datetime import datetime

from django.db.models import QuerySet
from django.db.transaction import atomic
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request

from app_user.models import User
from core.error_code import ECEnum
from core.response import response_ok
from libs.error_code.exception import ECException
from libs.dict import ExtDict


class UsersView(APIView):
    """用户"""

    def get(self, request: Request, *args, **kwargs) -> JsonResponse:
        """查看用户列表"""
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('perPage', 10))
        queryset: QuerySet = User.objects.filter(is_deleted=0). \
            only('user_id', 'name', 'user_type').order_by('-create_time')
        # 分页
        queryset = queryset[(page - 1) * per_page: page * per_page]
        data = []
        for obj in queryset:
            elem = ExtDict()
            elem.userId = obj.user_id
            elem.name = obj.name
            elem.userType = obj.user_type
            data.append(elem)
        return response_ok(data)

    @atomic()
    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        """新增用户"""
        name = request.data.get('name')
        if User.objects.filter(is_deleted=0, name=name).exists():
            raise ECException(ECEnum.UserExist)
        obj: User = User.objects.create(name=name)
        data = ExtDict()
        data.userId = obj.user_id
        data.name = obj.name
        data.userType = obj.user_type
        return response_ok(data)


class UserView(APIView):
    """单个用户"""

    def get(self, request: Request, user_id: str, *args, **kwargs):
        obj = User.objects.get(user_id=user_id)
        data = ExtDict()
        data.userId = obj.user_id
        data.name = obj.name
        data.userType = obj.user_type
        return response_ok(data)

    @atomic()
    def patch(self, request: Request, user_id: str, *args, **kwargs):
        name = request.data.get('name')
        now = datetime.now()
        if User.objects.exclude(user_id=user_id).filter(is_deleted=0, name=name).exists():
            raise ECException(ECEnum.UserExist)
        User.objects.filter(user_id=user_id).update(update_time=now, name=name)
        return response_ok()
