from django.shortcuts import get_list_or_404
from django.db import models


class Quest(models.Model):
    """ Опрос """

    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = u'Опрос'
        verbose_name_plural = u'Опросы'

    def __str__(self):
        return self.title



print(1)