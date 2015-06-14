# -*-coding: utf-8 -*-
import datetime
from annoying.decorators import ajax_request
from django.http import HttpResponse
from django.shortcuts import redirect
from Notes.models import Notes, Category
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.db.models import Q


def all_notes(request, username):
    if username != request.user.username:
        return redirect('')
    args = {}
    args.update(csrf(request))
    args['data'] = []
    for i in Notes.objects.all().filter(note_user=request.user):
        args['data'].insert(0, ([i.id,
                                 i.note_header,
                                 i.note_time,
                                 i.note_category,
                                 i.note_text,
                                 i.note_favorites]))
    t = loader.get_template('notes.html')
    c = RequestContext(request, args)
    return HttpResponse(t.render(c))


@ajax_request
def del_notes(request, username, id):
    if not(request.user.username == username or Notes.objects.all().filter(notes_user=request.user, id=id)):
        return 0
    else:
        Notes.objects.get(id=id).delete()
        return 1


@ajax_request
def red_notes(request, username, id):
    if not request.user.username == username or not (Notes.objects.all().filter(note_user=request.user, id=id)):
        return redirect('/')
    else:
        args = {}
        args.update(csrf(request))
        print(request.POST.get('text'))
        if request.POST.get('red'):
            farm = Notes.objects.get(id=id)
            farm.note_text = request.POST.get('text')
            farm.save()
            print("ok")
            return

        else:
            args['category_s'] = Category.objects.values().filter(category_user=1)
            if Category.objects.values().filter(category_user=request.user):
                args['category_m'] = Category.objects.values().filter(category_user=request.user)
            else:
                args['category_m'] = False
            args['data'] = Notes.objects.values().get(id=id)
            t = loader.get_template('note.html')
            c = RequestContext(request, args)
            return HttpResponse(t.render(c))


@ajax_request
def category_plus(request, username):
    if not request.user.username == username or not request.POST.get('category'):
        return redirect('/')
    else:
        farm = Category.objects.create(category_user=request.user, category_text=request.POST.get('category'))
        farm.save()
        return Category.objects.latest('id').id