# coding: utf-8

import time
from typing import Optional, Callable

from django.http import HttpResponse

from core.wsgi import ExtWSGIRequest
from .base import BaseMiddleware
from libs.logger_proxy import LoggerProxy

logger = LoggerProxy(__name__)


class TimerMiddleware(BaseMiddleware):

    key: str = 'start_time'
    threshold: float = 2.0

    def process_request(self, request: ExtWSGIRequest) -> None:
        setattr(request.ext, self.key, time.time())

    def process_view(self, request: ExtWSGIRequest, view_func: Callable, view_args: tuple, view_kwargs: dict) -> None:
        pass

    def process_exception(self, request: ExtWSGIRequest, exception: Exception) -> Optional[HttpResponse]:
        pass

    def process_response(self, request: ExtWSGIRequest, response: HttpResponse) -> HttpResponse:
        if hasattr(request.ext, self.key):
            diff = time.time() - getattr(request.ext, self.key)
            if diff > self.threshold:
                logger.warning('%s response timeout: %.6f' % (request.get_full_path(), diff))
        return response
