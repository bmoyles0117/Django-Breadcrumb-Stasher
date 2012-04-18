from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import redirect as django_redirect 
from django.conf import settings
from functools import wraps
import base64

def get_cookie_key():
    cookie_key = 'breadcrumb_stash'

    if hasattr(settings, 'BREADCRUMB_STASH_COOKIE_KEY'):
        cookie_key = settings.BREADCRUMB_STASH_COOKIE_KEY

    return cookie_key

def get_stash(request):
    return [x for x in base64.b64decode(request.session.get(get_cookie_key(), '')).split('|') if len(x)]

def redirect(request, *args, **kwargs):
    current_stash = get_stash(request)

    if len(current_stash):
        # Extract the target redirect
        target_redirect = current_stash.pop()

        # Update the stash
        set_stash(request, current_stash)

        return django_redirect(target_redirect)
    else:
        return django_redirect(*args, **kwargs)

def set_stash(request, breadcrumb_list):
    request.session[get_cookie_key()] = base64.b64encode('|'.join(breadcrumb_list))

    return True

def stash(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        current_stash = get_stash(request)

        current_stash.append(request.get_full_path())

        set_stash(request, current_stash)
        
        return func(request, *args, **kwargs)

    return inner