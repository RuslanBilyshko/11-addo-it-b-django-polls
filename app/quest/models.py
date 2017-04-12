from django.db import models
from django.shortcuts import get_object_or_404, get_list_or_404
from .forms import get_form
from django.contrib.auth.models import User

class Quest(models.Model):
    """ Опрос """

    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = u'Опрос'
        verbose_name_plural = u'Опросы'


    def __str__(self):
        return self.title


class Choise_type(models.Model):
    """ Тип ответа """

    type = models.CharField(max_length=50)
    label = models.CharField(max_length=100)

    class Meta:
        verbose_name = u'Тип ответа'
        verbose_name_plural = u'Типы ответов'

    def __str__(self):
        return self.label


class Question(models.Model):
    """ Вопрос """

    question_text = models.CharField(max_length=255)
    choise_type = models.ForeignKey(Choise_type, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Вопрос'
        verbose_name_plural = u'Вопросы'

    def __str__(self):
        return self.question_text


class Choise(models.Model):
    """ Вариант ответа """

    choice_text = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Вариант ответа'
        verbose_name_plural = u'Варианты ответов'

    def __str__(self):
        return self.choice_text


class Choise_result(models.Model):
    """ Результаты опросов """

    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choise = models.ForeignKey(Choise, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        verbose_name = u'Результат опроса'
        verbose_name_plural = u'Результаты опросов'

    def __str__(self):
        return "Результаты"
