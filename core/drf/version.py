# coding: utf-8

from rest_framework.exceptions import NotFound
from rest_framework.versioning import URLPathVersioning as OriginURLPathVersioning

from core.error_code import ECEnum
from libs.error_code.exception import ECException


class URLPathVersioning(OriginURLPathVersioning):
    """URLPathVersioning

    重写 determine_version
    """

    def determine_version(self, request, *args, **kwargs):
        try:
            return super(URLPathVersioning, self).determine_version(request, *args, **kwargs)
        except NotFound:
            raise ECException(ECEnum.InvalidVersion)
