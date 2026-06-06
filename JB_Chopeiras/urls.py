from django.urls import include, path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=False)),
    path('home/', views.home, name='home'),
    path('entrada/', views.tela_entrada, name='tela_entrada'),
    path('sair/', views.sair, name='sair'),
    path('clientes/', include('clientes.urls')),
    path('servicos/', include('servicos.urls')),
]