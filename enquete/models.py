# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
import datetime


class Pergunta(models.Model):
    descricao = models.CharField(max_length=200)
    data_publicacao = models.DateTimeField('date published')

    def __unicode__(self):
        return self.descricao

    def foi_publicado_recentemente(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.data_publicacao <= now


class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta)
    descricao = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __unicode__(self):
        return self.descricao
