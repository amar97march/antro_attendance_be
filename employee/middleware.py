
class IPAddressRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_ip = '127.0.0.1'
        client_ip = request.META.get('REMOTE_ADDR')
        if client_ip != allowed_ip:
            return HttpResponseForbidden("Access Forbidden")
        return self.get_response(request)