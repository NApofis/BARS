# -*-coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from Notes.views import all_notes
from Authenticated.views import register

urlpatterns = patterns('',
                        url(r'(?P<username>\w+)/$', all_notes),
                        url(r'', register),
                      )