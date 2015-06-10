# -*-coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
                       url(r'register/', 'Authenticated.views.register'),
                       url(r'login/', 'Authenticated.views.login'),
                       url(r'logout/', 'Authenticated.views.logout'),
                       url(r'notes/', include('Notes.urls')),
                       url(r'', 'Authenticated.views.paper'),
                      )