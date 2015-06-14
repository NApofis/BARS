# -*-coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from Notes.views import all_notes, del_notes, red_notes, category_plus
from Authenticated.views import register

urlpatterns = patterns('',
                        url(r'(?P<username>\w+)/del_(?P<id>\d+)/', del_notes),
                        url(r'(?P<username>\w+)/red_(?P<id>\d+)/', red_notes),
                        url(r'(?P<username>\w+)/category_plus/', category_plus),
                        url(r'(?P<username>\w+)/', all_notes),
                        url(r'', register),
                      )