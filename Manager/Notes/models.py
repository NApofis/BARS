# -*-coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User


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
    category_user = models.ForeignKey(User, default=None)


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

    note_time = models.TimeField(default=datetime.datetime.now())
    note_text = models.TextField()
    note_category = models.ForeignKey(Category)
    note_favorites = models.BooleanField(default=False)
    note_user = models.ForeignKey(User)
