from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('entrada/', views.tela_entrada, name='tela_entrada'),

    path('sair/', views.sair, name='sair'),

    path('formulario/', views.preencher_formulario, name='preencher_formulario'),

    path('formulario/sucesso/', views.formulario_sucesso, name='formulario_sucesso'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('relatorios/', views.relatorios, name='relatorios'),

    path('relatorios/gerar/', views.gerar_relatorio, name='gerar_relatorio'),

    path('relatorios/visualizar/', views.visualizar_relatorios, name='visualizar_relatorios'),

    path('clientes/', include('clientes.urls')),

    path('servicos/', include('servicos.urls')),

    path( 'configuracoes/', views.configuracoes, name='configuracoes'),
]