# Based on the implementation provided by scripts.mit.edu
# Link:  http://web.mit.edu/snippets/django/mit/

from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.middleware import PersistentRemoteUserMiddleware
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import reverse
from django.utils.http import is_safe_url
from django.http import HttpResponseRedirect

from django.conf import settings

class KerbRemoteUserMiddleware(PersistentRemoteUserMiddleware):
    header = 'SSL_CLIENT_S_DN_Email'

class KerbRemoteUserBackend(RemoteUserBackend):
    create_unknown_user=False

    def clean_username(self, username):
        if '@' in username:
            name, domain = username.split('@')
            assert(domain.upper() == 'MIT.EDU')
            return name
        else:
            return username

def generate_auth_login_redirect(request):
    '''
    Helper function that generates a HttpResponseRedirect to the default
    django.contrib.auth.view.LoginView view.
    '''

    query_string = '?' + request.GET.urlencode() if (len(request.GET) > 0) else ''
    login_url = reverse('login') + query_string
    return HttpResponseRedirect(login_url)

def kerb_login(request):
    '''
    Handle proper redirect to try and get user certificate. If this fails,
    redirect to standart login view.
    '''

    host = request.get_host().split(':')[0]

    if host in ('localhost', '127.0.0.1'):
        # Can't authenticate using certificate on localhost
        # Redirect to normal login page
        return generate_auth_login_redirect(request)

    if request.META['SERVER_PORT'] == '444':
        # Check if user is authenticated using certificate
        if not request.user.is_authenticated:
            # Not authenticated -> Present normal login website
            return generate_auth_login_redirect(request)

        # They're already authenticated --- go ahead and redirect
        redirect_to = request.GET.get(REDIRECT_FIELD_NAME, '')
        url_is_safe = is_safe_url(
            url = redirect_to,
            allowed_hosts = {request.get_host()},
            require_https = request.is_secure()
        )

        if (not redirect_to) or (not url_is_safe) or ('//' in redirect_to) or (' ' in redirect_to):
            redirect_to = settings.LOGIN_REDIRECT_URL

        # Force back to default https port
        redirect_to = f'https://{host}{redirect_to}'
        return HttpResponseRedirect(redirect_to)

    # Redirect to port 444 to get certificate authentification request
    redirect_to = f'https://{host}:444{request.get_full_path()}'
    return HttpResponseRedirect(redirect_to)

