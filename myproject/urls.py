"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from events import views
#from mains import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^photos/$', views.home, name='home'),
    #url(r'^index/', views.homeCall, name='site'),
    url(r'^Events/List/$', views.home, name='home'),
    url(r'^Book/Seats/$', views.book, name='book'),
    url(r'^Booked/Seats$', views.booked, name='booked'),
    url(r'^Booking/success/$', views.success, name='success'),
    url(r'^Booking/failure/$', views.failure, name='failure'),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
