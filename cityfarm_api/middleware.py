import threading
from django.http import Http404
from .urls import get_current_urls

request_cfg = threading.local()

class FarmRoutingMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        if 'farm' in view_kwargs:
            request_cfg.farm = view_kwargs['farm']

    def process_response(self, request, response):
        if hasattr(request_cfg, 'farm'):
            del request_cfg.farm
        return response

class FarmDbRouter:
    def db_for_read(self, model, **hints):
        if hasattr(request_cfg, 'farm'):
            return request_cfg.farm
        return 'default'
