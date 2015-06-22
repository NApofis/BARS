# -*-coding: utf-8 -*-
from annoying.decorators import ajax_request
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from Notes.models import Notes, Category
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from Notes.forms import Note
from django.template.defaultfilters import date as _date

def all_notes(request, username):
    """
    Проверяет валидность присланных данных и возвращает список заметок пользователя и его категории
    если данные валидны лил отправляет на страницу для вызова фунуции Authenticated.paper есди данные не валидны.
    :param request:
    :param username:
    :return: render_to_response(Notes.html, RequestContext(request(param), args(список)) or redirect('/'):
    """
    if username != request.user.username:
        return redirect('/')
    args = {}
    args.update(csrf(request))
    args['data'] = []
    farm = Note
    args['form'] = farm
    for i in Notes.objects.all().filter(note_user=request.user):
        e = 0
        if i.uuid_boolean:
            print request
            e = "http://127.0.0.1:8100" + i.get_absolute_url()
        args['data'].insert(0, ([i.id,
                                 i.note_header,
                                 i.note_time,
                                 i.note_category,
                                 i.note_text,
                                 i.note_favorites,
                                 e]))
    args['category_s'] = Category.objects.values().filter(category_user=1)
    if Category.objects.values().filter(category_user=request.user):
        args['category_m'] = Category.objects.values().filter(category_user=request.user)
    else:
        args['category_m'] = False
    t = loader.get_template('notes.html')
    c = RequestContext(request, args)
    return HttpResponse(t.render(c))

@ajax_request
def del_note(request, username, id):
    """
    Проверяет присланные данные на валидность и возвращает True если закладка удалена или 'error' если данные не валидны.
    :param request:
    :param username:
    :param id:
    :return 1 or 'error':
    """
    if not request.user.username == username:
        return 'error'
    else:
        try:
            Notes.objects.get(pk=id).delete()
            return 1
        except Notes.DoesNotExist:
            return 'error'

@ajax_request
def new_note(request, username, id):
    """
    Проверяет присланные данные на валидность и возвращает True если закладка была отредактирована или
    args(список) если была добавлена новая закладко. Если данные не валидны возвращает 'error'.
    :param request:
    :param username:
    :param id:
    :return args(список) or 1 or 'error':
    """
    if not request.user.username == username:
        return 'error'
    else:
        favorites = 1 if request.POST.get('favorites') == "true" else 0
        category = Category.objects.get(pk=request.POST.get('category'))
        try:
            farm = Notes.objects.get(pk=id)
            farm.note_text = request.POST.get('text')
            farm.note_header = request.POST.get('header')
            farm.note_category = category
            farm.note_favorites = favorites
            farm.save()
            return 1
        except Notes.DoesNotExist:
            if request.method == 'POST' and id == "0":
                farm = Notes.objects.create(note_user=request.user,
                                            note_text=request.POST.get('text'),
                                            note_header=request.POST.get('header'),
                                            note_favorites=favorites,
                                            note_category=category
                )
                farm.save()
                time = _date(farm.note_time, "d E Y г. G:i")
                args = {'data': 0, 'pk': farm.pk, 'tim': time}
                return args
            else:
                return 'error'

@ajax_request
def category_plus(request, username):
    """
    Проверяет данные на валитность и вовращает args(словарь) с значением 'stat' == 1 если категория добавлена и
    'stat' == 0 если данная категория у этого пользователя существует. Если данные не валидны возвращает 'error'.
    :param request:
    :param username:
    :return 'error' or args(словарь):
    """
    if not request.user.username == username or not request.POST.get('category'):
        return 'error'
    else:
        try:
            Category.objects.get(category_text=request.POST.get('category'))
            return {'stat':0}
        except Category.DoesNotExist:
            farm = Category.objects.create(category_user=request.user, category_text=request.POST.get('category'))
            farm.save()
            return {'stat': 1, 'id': Category.objects.latest('id').id}

@ajax_request
def category_del(request, username):
    """
    Проверяет данные на валидность и возвращает args(словарь) c значением 'stat' == 0 если данной категории не существет
    и 'stat' == 1 если категория удалена и все заметки относящиеся к данной категории. Если данные не валидны возвращает
    'error'.
    :param request:
    :param username:
    :return args(словарь) or 'error:
    """
    if not request.user.username == username or not request.POST.get('category'):
        return 'error'
    else:
        try:
            category = Category.objects.get(category_text=request.POST.get('category'))
            notes = Notes.objects.filter(note_category=category)
            notes.delete()
            id = category.id
            category.delete()
            return {'stat': 1, 'id': id}
        except Category.DoesNotExist:
            return {'stat': 0}

@ajax_request
def sorted_notes(request, username):
    """
    Проверяет данные на валидность и возвращает args(список) c отсортироваными id заметок относительно присланных данных
    Если данные не валидны тогда возвращает 'error'.
    :param request:
    :param username:
    :return 'error' or args(список):
    """
    if not request.user.username == username or not request.POST.get('s_category') \
            or not request.POST.get('s_cret'):
        return 'error'
    else:
        args = []
        if request.POST.get('s_category') == '1':
            m = "" if request.POST.get('s_cret') == '1' else "-"
            m += "note_time"
        elif request.POST.get('s_category') == '2':
            m = "" if request.POST.get('s_cret') == '1' else "-"
            m += "note_category"
        elif request.POST.get('s_category') == '3':
            m = "" if request.POST.get('s_cret') == '1' else "-"
            m += "note_favorites"
        else:
            return 'error'
        farm = Notes.objects.filter(note_user=request.user).order_by(m)
        for i in farm:
            args.append(i.id)
        return args

@ajax_request
def search_note(request, username):
    """
    Проверяет данные на валидность и возвращает args(список) с id заметок которые подходят под выбраные параметры.
    Если заметок подходящих под выюраные параметры нет тогда возвращает 'not'. Если данные не валидны возвращает 'error'.
    :param request:
    :param username:
    :return args(список) or 'not' or 'error':
    """
    if not request.user.username == username or not request.POST.get('idi') \
            or not request.POST.get('data'):
        return 'error'
    else:
        args = []
        if request.POST.get('idi') == '1':
            d = request.POST.get('data')[0:2]
            m = request.POST.get('data')[3:5]
            y = request.POST.get('data')[6:]
            date = y + '-' + m + '-' + d
            if len(Notes.objects.filter(note_user=request.user, note_date=date)) > 0:
                farm = Notes.objects.filter(note_user=request.user, note_date=date)
                for i in farm:
                    args.append(i.id)
                return args
            else:
                return 'not'
        elif request.POST.get('idi') == '2':
            print 2
            if Notes.objects.filter(note_user=request.user, note_header=request.POST.get('data')):
                farm = Notes.objects.filter(note_user=request.user, note_header=request.POST.get('data'))
                for i in farm:
                    args.append(i.id)
                return args
            else:
                return 'not'
        elif request.POST.get('idi') == '3':
            print 3
            if Notes.objects.filter(note_user=request.user, note_category=request.POST.get('data')):
                farm = Notes.objects.filter(note_user=request.user, note_category=request.POST.get('data'))
                for i in farm:
                    args.append(i.id)
                return args
            else:
                return 'not'
        elif request.POST.get('idi') == '4':
            print 4
            f = 1 if request.POST.get('data') == "1" else 0
            if Notes.objects.filter(note_user=request.user, note_favorites=f):
                farm = Notes.objects.filter(note_user=request.user, note_favorites=f)
                for i in farm:
                    args.append(i.id)
                return args
            else:
                return 'not'
        else:
            return 'not'

@ajax_request
def href_open_note(request, username, id):
    """
    Проверяет данные на валидность и возвращает url для заметки и открывает общий доступ к данной заметки.
    Если данные не валидны  возвращает 'error'.
    :param request:
    :param username:
    :param id:
    :return 'error' or get_absolute_url():
    """
    if not request.user.username == username:
        return 'error'
    else:
        try:
            farm = Notes.objects.get(note_user=request.user, id=id)
            farm.uuid_boolean = 1
            farm.save()
            return farm.get_absolute_url()
        except Notes.DoesNotExist:
            return 'error'

@ajax_request
def href_close_note(request, username, id):
    """
    Проверяет данные на валидность и возвращает True если общий доступ к заметки закрыт.
    Если данные не валидны  возвращает 'error'.
    :param request:
    :param username:
    :param id:
    :return 1 or 'error':
    """
    if not request.user.username == username:
        return 'error'
    else:
        try:
            farm = Notes.objects.get(note_user=request.user, id=id)
            farm.uuid_boolean = 0
            farm.save()
            return 1
        except Notes.DoesNotExist:
            return 'error'

def his_note(request, uuid):
    """
    Проверяет данные на валидность и возвращает args(список). Если общий доступ для заметки открыт тогда в args
    добавляется текст заметки если доступ закрыт возвращается сообветствующее сообщение. Если данной заметки не
    существует тогда вернет соответстующее сообщение.
    :param request:
    :param uuid:
    :return render_to_response('note.html',RequestContext(request(param), args(список)):
    """
    try:
        farm = Notes.objects.get(uuid=uuid)
        args = {}
        args.update(csrf(request))
        print uuid
        if farm.uuid_boolean:
            args['note'] = farm.note_text
        else:
            args['note'] = "Извените. Для данной заметки закрыт доступ."
    except Notes.DoesNotExist:
        args['note'] = "Url адрес не верный"
    c = RequestContext(request, args)
    return render_to_response('note.html', c)