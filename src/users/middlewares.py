from datetime import datetime


class UserLastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        if request.user.is_authenticated:
            request.user.last_request = datetime.utcnow()
            request.user.save()
        return response
