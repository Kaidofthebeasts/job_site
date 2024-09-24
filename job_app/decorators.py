from django.http import Http404
from django.contrib.auth.decorators import user_passes_test


def staff_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_staff,
        login_url='/404/'
    )(view_func)
    return decorated_view_func
