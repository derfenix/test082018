from typing import Callable

from django.http import HttpRequest, HttpResponseForbidden

from test082018.local_storage import storage


def current_user_id_middleware(get_response: Callable):
    def middleware(request: HttpRequest):
        try:
            storage.set_user_id(request.GET['user_id'])
        except (TypeError, ValueError, KeyError):
            return HttpResponseForbidden()
        return get_response(request)
    return middleware
