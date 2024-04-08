from django.http import HttpResponseForbidden
from django.urls import reverse
from employee.models import AllowedIP


class IPAddressRestrictionMiddleware:

    """
    Middleware to restrict access based on IP address.

    This middleware allows only requests from a specific IP address.
    """  


    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define the allowed IP for accessing the admin dashboard
        admin_allowed_ip = '127.0.0.1'
        # Define the allowed IPs for accessing APIs
        api_allowed_ips = [i.ip for i in AllowedIP.objects.all()]  # Add more IPs as needed
        
        # Get client's IP address
        client_ip = request.META.get('REMOTE_ADDR')
        
        # Check if the request is for admin dashboard
        if request.path.startswith(reverse('admin:index')):
            # Allow access if the client's IP matches the allowed IP
            pass
            # if client_ip != admin_allowed_ip:
            #     return HttpResponseForbidden("Access Forbidden")
        # Check if the request is for APIs
        elif request.path.startswith('/api/'):
            # Deny access if the client's IP is not in the allowed IPs list
            if client_ip not in api_allowed_ips:
                return HttpResponseForbidden("Access Forbidden")
        
        # Allow access for all other requests
        return self.get_response(request)