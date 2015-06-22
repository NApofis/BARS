# -*-coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
from uuidfield import UUIDField


class Category(models.Model):
    """
    Category
    Создает таблицу для базы данных.
    """
    class Meta():
        """
        Meta
        Присваивает названию таблицы значение category.
        """
        db_table = 'category'

    category_text = models.CharField(max_length=250)
    category_user = models.ForeignKey(User)

    def __unicode__(self):
        return self.category_text


class Notes(models.Model):
    """
    Notes
    Создает таблицу для базы данных.
    """
    class Meta():
        """
        Meta
        Присваивает названию таблицы значение notes.
        """
        db_table = 'notes'

    uuid = UUIDField(auto=True)
    uuid_boolean = models.BooleanField(default=False)
    note_header = models.CharField(max_length=250)
    note_time = models.DateTimeField(default=datetime.datetime.now())
    note_date = models.DateField(default=datetime.datetime.now())
    note_text = models.TextField(("Заметка"), blank=True, null=True)
    note_favorites = models.BooleanField(default=False)
    note_user = models.ForeignKey(User)
    note_category = models.ForeignKey(Category)

    def get_absolute_url(self):
        """
        Создает url для модели Notes со значением поля uuid
        :return:
        """
        return '/notes/note/{}/'.format(self.uuid)
