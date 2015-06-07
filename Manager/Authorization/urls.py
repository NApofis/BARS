# -*-coding: utf-8 -*-
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
                       url(r'register/', 'Authorization.views.register'),
                       url(r'login/', 'Authorization.views.login'),
                       url(r'logout/', 'Authorization.views.logout'),
                       url(r'notes/', include('Notes.urls')),
                       url(r'', 'Authorization.views.paper'),
                      )