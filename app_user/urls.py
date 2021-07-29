# coding: utf-8

from django.urls import path
from .views.user import test


urlpatterns = [
    path('test/', test)
]
