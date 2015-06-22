# -*-coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from Authenticated.views import register, logout, login, paper


urlpatterns = patterns('',
                       url(r'register/', register),
                       url(r'login/', login),
                       url(r'logout/', logout),
                       url(r'notes/', include('Notes.urls')),
                       url(r'', paper),
                      )