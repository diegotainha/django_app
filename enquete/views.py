# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import *


class IndexView(generic.ListView):
    # (padrão) template_name = 'enquete_list.html'
    template_name = 'enquete/index.html'

    # (padrão) context_object_name = 'pergunta_list'
    context_object_name = 'lista_ultimas_perguntas'

    def get_queryset(self):
        # retorna as ultmas 5 questões cadastradas
        return Pergunta.objects.filter(data_publicacao__lte=timezone.now()).order_by('data_publicacao')[:5]


class DetalhesView(generic.DetailView):
    model = Pergunta

    ''' (padrão) template_name = 'pergunta_detail.html' - onde 'pergunta' é nome do model referenciado
                                                             e 'detail' vem da view generica DetailView'''
    template_name = 'enquete/detalhe.html'

    def get_queryset(self):
        # Tira qualquer questão futura
        return Pergunta.objects.filter(data_publicacao__lte=timezone.now())


class ResultadoView(generic.DetailView):
    model = Pergunta
    # template_name pode ser definido no URLconf: views.ResultadoView.as_view(template_name='enquete/resultado.html'

    ''' (padrão) template_name = 'pergunta_detail.html' - onde 'pergunta' é nome do model referenciado
                                                             e 'detail' vem da view generica DetailView'''
    template_name = 'enquete/resultado.html'


def voto(request, pergunta_id):
    p = get_object_or_404(Pergunta, pk=pergunta_id)
    try:
        selected_resposta = p.resposta_set.get(pk=request.POST['resposta'])
    except (KeyError, Resposta.DoesNotExist):
        # Mostra novamente a página de votação
        return render(request, 'enquete/detalhe.html', {
            'pergunta': p,
            'error_message': "Selecione uma das questões disponíveis!",
        })
    else:
        selected_resposta.votos += 1
        selected_resposta.save()
        # Sempre retornar um HttpResponseRedirect depois de manipular dados
        # via POST com sucesso. Isso impede que dados sejam enviados duas vezes caso um
        # usuario clique no botão de volar do navegador.
        return HttpResponseRedirect(reverse('enquete:resultado', args=(p.id,)))
