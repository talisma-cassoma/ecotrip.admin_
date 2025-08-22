from django.conf import settings
from django.shortcuts import redirect
from django.utils import translation

def root_redirect_set_cookie(request):
    lang = (
        request.GET.get("lang")
        or request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        or translation.get_language_from_request(request)
    )
    translation.activate(lang)

    next_url = "/admin/" if request.user.is_authenticated else "/admin/login/"
    resp = redirect(next_url)
    resp.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)  # persiste a escolha
    return resp
