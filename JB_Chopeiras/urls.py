from django.urls import path, include
from . import views

urlpatterns = [

    path('relatorios/', views.relatorios, name='relatorios'),

    path('relatorios/gerar/', views.gerar_relatorio, name='gerar_relatorio'),

    path('relatorios/visualizar/', views.visualizar_relatorios, name='visualizar_relatorios'),

    path( 'configuracoes/', views.configuracoes, name='configuracoes'),
]
