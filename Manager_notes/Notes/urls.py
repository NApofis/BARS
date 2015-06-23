# -*-coding: utf-8 -*-
from django.conf.urls import patterns, url
from Notes.views import all_notes, del_note, new_note, category_plus, category_del, sorted_notes, search_note, \
    his_note, href_open_note, href_close_note
from Authenticated.views import paper

urlpatterns = patterns('',
                        url(r'(?P<username>\w+)/del_(?P<id>\d+)/', del_note),
                        url(r'(?P<username>\w+)/new_(?P<id>\d+)/', new_note),
                        url(r'(?P<username>\w+)/href_open_(?P<id>\d+)/', href_open_note),
                        url(r'(?P<username>\w+)/href_close_(?P<id>\d+)/', href_close_note),
                        url(r'(?P<username>\w+)/category_plus/', category_plus),
                        url(r'(?P<username>\w+)/category_del/', category_del),
                        url(r'(?P<username>\w+)/sorted/', sorted_notes),
                        url(r'(?P<username>\w+)/search/', search_note),
                        url(r'note/(?P<uuid>\w+)/', his_note),
                        url(r'(?P<username>\w+)/', all_notes),
                        url(r'', paper),
                      )