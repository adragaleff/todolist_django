from django.db import models
from datetime import datetime

from django.contrib.auth.models import User


class Task(models.Model):

    Priority = (
        ('Легкий', 'Легкий'),
        ('Обычный', 'Обычный'),
        ('Сложный', 'Сложный')
    )

    name = models.TextField('Название задачи', blank=True, null=True)
    description = models.TextField('Описание задачи', blank=True, null=True)
    owner = models.TextField('Создатель', blank=True, null=True)
    priority = models.CharField('Приоритет', choices=Priority, blank=True, max_length=50, default="Обычный")
    date_create = models.DateTimeField('Дата создания', blank=True, null=True, default=datetime.now())
    date_of_staging = models.DateTimeField('Дата сдачи', blank=True, null=True, default=datetime.now())
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Исполнитель', related_name='executed_tasks')
    is_archive = models.CharField('Статус архива', blank=True, null=False,max_length=5, default='0')

class License(models.Model):
    
    login = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Логин', related_name='login_user')
    token = models.TextField('Токен', blank=True, null=True, max_length=100)
    war_token = models.TextField('Боевой токен', blank=True, null=True, max_length=100)
    telegram_id = models.TextField('Telegram ID', blank=True, null=True, max_length=100)

class CommentsTask(models.Model):

    login = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.TextField('Комментарий')
    task_id = models.CharField('Номер задачи', blank=True, null=True, max_length=255)
