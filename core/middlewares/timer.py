# coding: utf-8

import time
import logging
from typing import Optional, Callable

from django.http import HttpResponse

from core.wsgi import ExtWSGIRequest
from .base import BaseMiddleware

log = logging.getLogger(__name__)


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
                log.warning('response timeout: %.6f' % diff)
        return response
