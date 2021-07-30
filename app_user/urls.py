# coding: utf-8

from django.urls import re_path, path
from .views.user import UsersView


# demo
urlpatterns = [
    path('', UsersView.as_view(), name='users')
]
