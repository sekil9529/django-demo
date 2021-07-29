# coding: utf-8

from django.urls import path
from .views.demo import hello, error_unknown, error_test


# demo
urlpatterns = [
    path('demo/hello', hello),
    path('demo/error/unknown', error_unknown),
    path('demo/error/test', error_test),
]
