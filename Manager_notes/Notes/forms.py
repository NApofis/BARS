# -*-coding: utf-8 -*-
from django.forms import ModelForm
from Notes.models import Notes


class Note(ModelForm):
    """
    Note
    Форма со строками базы данных.
    """
    class Meta():
        """
        Meta
        Выбор таблицы базы данных и выбор поля note_text.
        """
        model = Notes
        fields = ['note_text']


    class Media:
        """
        Подключение файлов javascript для tinymce редактора
        """
        js = ('/static/js/tiny_mce/tiny_mce.js',
              '/static/js/tiny_mce/textareas.js',
            )