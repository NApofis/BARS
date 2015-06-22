# -*-coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.template.context import RequestContext


def paper(request):
    """
    paper
    Проверяет авторизован пользователь или нет, если нет то отправляет на
    ввод логина и пароля, если да то отправляет на страницу с его заметками.
    :param request:
    :return redirect('/notes/(?P<username>\w+)/') or redirect('/auth/login/'):
    """
    if request.user.is_authenticated():
        r = '/notes/' + request.user.username + '/'
        return redirect(r)
    else:
        return redirect('/auth/login/')


def login(request):
    """
    login
    Проверяет веденный пользователем логин и пароль если пароль и логин подходят
    авторизует пользователя и отправляет на страницу с его заметками если пароль и логин
    не подходит или пользователь отправил пустую форму то отправляет на страницу
    ввода логина и пароля.
    :param request:
    :return: redirect('/notes/(?P<username>\w+)/') or render_to_response('login.html',
                                                                        RequestContext(request(param), args(список))):
    """
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            r = '/notes/' + request.user.username + '/'
            return redirect(r)
        else:
            c = RequestContext(request, args)
            args['login_error'] = 'Пользователь не существует'
            return render_to_response('login.html', c)
    else:
        c = RequestContext(request, args)
        return render_to_response('login.html', c)


def logout(request):
    """
    logout
    Выводит пользователя из авторизованного режима и перебрасывает на страницу
    для вызова функции paper.
    :param request:
    :return redirect('/'):
    """
    auth.logout(request)
    response = redirect('/')
    return response


def register(request):
    """
    register
    Регистрирует пользователя проверяя валидность его данных если данные валидны
    то отправляет на страницу для вызова функции paper если нет то отправляет на страницу регистрации.
    :param request:
    :return redirect('/') or render_to_response('register.html', RequestContext(request(param), args(список))):
    """
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm
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
    c = RequestContext(request, args)
    return render_to_response('register.html', c)
