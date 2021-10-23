# coding: utf-8

from django.urls import re_path, path
from .views.user import UsersView, UserView
from .views.user import users_list


# demo
urlpatterns = [
    path('', UsersView.as_view(), name='users'),
    path('list/', users_list, name='users_list'),
    re_path('^(?P<user_id>[0-9a-zA-Z]+)/$', UserView.as_view(), name='user')
]
