from django.contrib import admin
from .models import *


class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'data_publicacao')
    ordering = ('id',)


class RespostaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'votos', 'pergunta')
    ordering = ('pergunta', 'id',)


admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Resposta, RespostaAdmin)
