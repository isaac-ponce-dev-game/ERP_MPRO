# -*- coding: utf-8 -*-

from django.urls import re_path, include
from django.contrib import admin
from django.conf.urls.static import static
from .configs.settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^', include('erp_mpro.apps.base.urls')),
    re_path(r'^login/', include('erp_mpro.apps.login.urls')),
    re_path(r'^cadastro/', include('erp_mpro.apps.cadastro.urls')),
    re_path(r'^fiscal/', include('erp_mpro.apps.fiscal.urls')),
    re_path(r'^vendas/', include('erp_mpro.apps.vendas.urls')),
    re_path(r'^compras/', include('erp_mpro.apps.compras.urls')),
    re_path(r'^financeiro/', include('erp_mpro.apps.financeiro.urls')),
    re_path(r'^estoque/', include('erp_mpro.apps.estoque.urls')),
    
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
