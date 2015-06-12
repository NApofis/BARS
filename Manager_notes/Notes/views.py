# -*-coding: utf-8 -*-
import datetime
from annoying.decorators import ajax_request
from django.http import HttpResponse
from django.shortcuts import redirect
from Notes.models import Notes
from django.template import RequestContext, loader
from django.core.context_processors import csrf


def all_notes(request, username):
    if username != request.user.username:
        return redirect('')
    args = {}
    args.update(csrf(request))
    args['data'] = []
    for i in Notes.objects.all().filter(note_user=request.user):
        args['data'].insert(0, ([i.note_header,
                                 i.note_time,
                                 i.note_category,
                                 i.note_text,
                                 i.note_favorites]))
    t = loader.get_template('notes.html')
    c = RequestContext(request, args)
    return HttpResponse(t.render(c))
