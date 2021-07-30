# coding: utf-8

from django.urls import path
from .views import hello, error_unknown, error_test


urlpatterns = [
    path('hello/', hello),
    path('error/unknown/', error_unknown),
    path('error/test/', error_test),
]
