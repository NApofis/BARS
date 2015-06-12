# -*-coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.template.context import RequestContext


def paper(request):
    if request.user.is_authenticated():
        r = '/notes/' + request.user.username + '/'
        return redirect(r)
    else:
        return redirect('/auth/login/')


def login(request):
    args = {}
    args.update(csrf(request))
    c = RequestContext(request, args)
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            r = '/notes/' + request.user.username + '/'
            return redirect(r)
        else:
            args['login_error'] = 'Пользователь не существует'
            return render_to_response('login.html', c)
    else:
        return render_to_response('login.html', c)


def logout(request):
    auth.logout(request)
    response = redirect('/')
    return response


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm
    c = RequestContext(request, args)
    if request.POST:
        new_form = UserCreationForm(request.POST)
        if new_form.is_valid():
            new_form.save()
            newer = auth.authenticate(
                username=new_form.cleaned_data['username'],
                password=new_form.cleaned_data['password2']
            )
            auth.login(request, newer)
            return redirect('/')
        else:
            args['form'] = new_form
    return render_to_response('register.html', c)
