# -*-coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm


def paper(request):
    """
    paper
    Проверяет авторизован пользователь или нет, если нет то отправляет на
    ввод логина и пароля, если да то отправляет в общий чат.
    :param request:
    :return redirect('/article/') or redirect('/auth/login/'):
    """
    if request.user.is_authenticated():
        return redirect('/notes/')
    else:
        return redirect('/auth/login/')


def login(request):
    """
    login
    Проверяет веденный пользователем логин и пароль если пароль и логин подходят
    авторизует пользователя и отправляет в общий чат если пароль и логин
    не подходит или пользователь отправил пустую форму то отправляет на страницу
    ввода логина и пароля.
    :param request:
    :return redirect('/article/') or
                                render_to_response('login.html', args(список)):
    """
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/notes/')
        else:
            args['login_error'] = 'Пользователь не существует'
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)


def logout(request):
    """
    logout
    Выводит пользователя из авторизованного режима и перебрасывает на страницу
    ввода логина и пароля.
    :param request:
    :return redirect('/'):
    """
    auth.logout(request)
    response = redirect('/')
    return response


def delet(request):
    """
    :param request:
    :return: redirect('/')
    """
    auth.logout(request)


def register(request):
    """
    register
    Регистрирует пользователя проверяя валидность его данных если данные валидны
    то отправляет в общий чаь если нет то отправляет на страницу регистрации.
    :param request:
    :return redirect('/') or render_to_response('register.html', args(список)):
    """
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm
    if request.POST:
        newer_form = UserCreationForm(request.POST)
        if newer_form.is_valid():
            newer_form.save()
            newer = auth.authenticate(
                username=newer_form.cleaned_data['username'],
                password=newer_form.cleaned_data['password2']
            )
            auth.login(request, newer)
            response = redirect('/')
            return response
        else:
            args['form'] = newer_form
    return render_to_response('register.html', args)
# Create your views here.
