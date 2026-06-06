from django.urls import include, path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('entrada/', views.tela_entrada, name='tela_entrada'),
    path('sair/', views.sair, name='sair'),
    path('clientes/', include('clientes.urls')),
    path('servicos/', include('servicos.urls')),
]