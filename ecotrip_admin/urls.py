from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from .views import root_redirect_set_cookie

urlpatterns = [
    # rota para trocar idioma
    path("i18n/", include("django.conf.urls.i18n")),  # continua disponível p/ outras telas
    path("", root_redirect_set_cookie, name="root"),
    path("admin/", admin.site.urls),
    path('', lambda request: redirect('/admin/', permanent=False)), # redirecionar o user para /admin
    # admin normal (sem i18n_patterns para não quebrar login/logout)
]
