from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('entrada/', views.tela_entrada, name='tela_entrada'),
    path('sair/', views.sair, name='sair'),
]
