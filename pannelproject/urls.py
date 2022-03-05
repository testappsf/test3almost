"""pannelproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from cgitb import handler
from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from Dashboard import views as v
from django.views.generic import TemplateView

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', TemplateView.as_view(template_name="blog/home.html"),name='/'),
    path('about/', TemplateView.as_view(template_name="blog/about.html"),name='about'),
    path('contact/', TemplateView.as_view(template_name="blog/contact.html"),name='contact'),
    path('services/', TemplateView.as_view(template_name="blog/service.html"),name='services'),
    path('redirect/',include('Dashboard.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    
]
urlpatterns=urlpatterns+staticfiles_urlpatterns()
urlpatterns=urlpatterns+static(settings.MEDIA_URL,
                               document_root=settings.MEDIA_ROOT)

handler404= 'Dashboard.views.error_404_view'

import re
IGNORABLE_404_URLS = [
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
]