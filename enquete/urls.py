# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^e/(?P<pk>[0-9]+)/$', views.DetalhesView.as_view(), name='detalhes'),

    url(r'^e/(?P<pk>[0-9]+)/resultado/$', views.ResultadoView.as_view(), name='resultado'),

    url(r'^e/(?P<pergunta_id>[0-9]+)/voto/$', views.voto, name='voto'),
]
