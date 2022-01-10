from django.http import HttpResponseRedirect
from django.urls import reverse

import re

class CreateProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        self.create_profile_path = reverse('home:create_profile')
        self.logout_path = reverse('logout')
        self.admin_re = re.compile(r'^/admin/?')

    def __call__(self, request):
        if request.user.is_authenticated and request.path != self.create_profile_path and request.path != self.logout_path and not self.admin_re.match(request.path):
            if not hasattr(request.user, 'member'):
                # Force user to create a profile
                return HttpResponseRedirect(self.create_profile_path)

        response = self.get_response(request)
        return response