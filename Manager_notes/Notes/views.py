from django.shortcuts import render, render_to_response
from django.template import RequestContext


def paper(request):
    c = RequestContext(request)
    return render_to_response('notes.html', c)
