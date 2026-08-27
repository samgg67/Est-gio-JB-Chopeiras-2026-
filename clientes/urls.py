from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientesPage, name='clientesPage'),
    path('criar/',views.criar_cliente,name='criar_cliente'),
    path('editar/<int:id>/',views.editar_cliente,name='editar_cliente'),
    path('detalhes/<int:id>/',views.detalhes_cliente,name='detalhes_cliente'),
    path('inativar/<int:id>/',views.inativar_cliente,name='inativar_cliente'),
    path('reativar/<int:id>/',views.reativar_cliente,name='reativar_cliente'),
]