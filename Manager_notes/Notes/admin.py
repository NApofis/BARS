# -*-coding: utf-8 -*-
from django.contrib import admin
from Notes.models import Notes, Category
from django.contrib.auth.models import User


class Art(admin.ModelAdmin):
    """
    Создание класса для админ панели.
    """
    class Media:
        """
        Подключение javascript файлов для tinymce редактора
        """
        js = ('/static/js/tiny_mce/tiny_mce.js',
              '/static/js/tiny_mce/textareas.js'
            )

admin.site.register(Notes, Art)
admin.site.register(Category)
# Register your models here.
