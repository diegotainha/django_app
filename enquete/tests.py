# -*- coding: utf-8 -*-

import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Pergunta


class PerguntaMethodTests(TestCase):
    def teste_foi_publicado_recentemente_com_pergunta_futura(self):
        # metodo 'foi_publicado_recentemente' deve retornar False para Perguntas com datas futuras
        time = timezone.now() + datetime.timedelta(days=30)
        pergunta_futura = Pergunta(data_publicacao=time)
        self.assertEqual(pergunta_futura.foi_publicado_recentemente(), False)

    def teste_foi_publicado_recentemente_com_perguntas_antigas(self):
        # metodo 'foi_publicado_recentemente' deve retornar Falso para perguntas com mais de 1 dia
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Pergunta(data_publicacao=time)
        self.assertEqual(old_question.foi_publicado_recentemente(), False)

    def teste_foi_publicado_recentemente_com_perguntas_recentes(self):
        # metodo 'foi_publicado_recentemente' deve retornar True para Perguntas do ultimo dia (recentes)
        time = timezone.now() - datetime.timedelta(hours=1)
        pergunta_recente = Pergunta(data_publicacao=time)
        self.assertEqual(pergunta_recente.foi_publicado_recentemente(), True)


def criar_pergunta(descricao, dias):
    time = timezone.now() + datetime.timedelta(days=dias)
    return Pergunta.objects.create(descricao=descricao, data_publicacao=time)


class PerguntaViewTests(TestCase):
    def teste_index_view_sem_perguntas(self):
        # Se não existem Perguntas deve ser apresentada uma mensagem apropriada
        response = self.client.get(reverse('enquete:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ainda não existem pesquisas.")  # texto que da pagina index.html
        self.assertQuerysetEqual(response.context['lista_ultimas_perguntas'], [])

    def teste_index_view_com_perguntas_antigas(self):
        # Perguntas com data no passado serão mostradas
        criar_pergunta(descricao="Pergunta no passado.", dias=-30)
        response = self.client.get(reverse('enquete:index'))
        self.assertQuerysetEqual(
            response.context['lista_ultimas_perguntas'],
            ['<Pergunta: Pergunta no passado.>']
        )

    def teste_index_view_com_pergunta_futura(self):
        # Perguntas com data futura não devem ser apresentadas
        criar_pergunta(descricao="Pergunta no futuro.", dias=30)
        response = self.client.get(reverse('enquete:index'))
        self.assertContains(response, "Ainda não existem pesquisas.", status_code=200)  # texto da pagina index.html
        self.assertQuerysetEqual(response.context['lista_ultimas_perguntas'], [])

    def test_index_view_com_perguntas_futuras_e_antigas(self):
        # Mesmo se perguntas antigas e futras existirem serão apresentas apenas as antigas
        criar_pergunta(descricao="Pergunta antiga.", dias=-30)
        criar_pergunta(descricao="Pergunta futura.", dias=30)
        response = self.client.get(reverse('enquete:index'))
        self.assertQuerysetEqual(
            response.context['lista_ultimas_perguntas'],
            ['<Pergunta: Pergunta antiga.>']
        )

    def test_index_view_with_two_past_questions(self):
        # Apresentar varias Perguntas na pagina index
        criar_pergunta(descricao="Pergunta antiga 1.", dias=-30)
        criar_pergunta(descricao="Pergunta antiga 2.", dias=-5)
        response = self.client.get(reverse('enquete:index'))
        self.assertQuerysetEqual(
            response.context['lista_ultimas_perguntas'],
            ['<Pergunta: Pergunta antiga 1.>', '<Pergunta: Pergunta antiga 2.>']
        )


class PerguntaIndexDetalhesTests(TestCase):
    def teste_view_detalhe_com_pergunta_futura(self):
        # A view Detalhe deve retornar 404 para perguntas no futuro
        pergunta_futura = criar_pergunta(descricao="Pergunta futura.", dias=5)
        response = self.client.get(reverse('enquete:detalhes', args=(pergunta_futura.id,)))
        self.assertEqual(response.status_code, 404)

    def teste_view_detalhe_com_pergunta_antiga(self):
        # A view Detalhe deve exibir o texto da pergunta que está com data antiga
        pergunta_antiga = criar_pergunta(descricao="Pergunta antiga.", dias=-5)
        response = self.client.get(reverse('enquete:detalhes', args=(pergunta_antiga.id,)))
        self.assertContains(response, pergunta_antiga.descricao, status_code=200)
