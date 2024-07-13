from django.db import close_old_connections

class CloseConnectionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        close_old_connections()
        return response