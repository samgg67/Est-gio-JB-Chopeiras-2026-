from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientesPage, name='clientesPage'),
    path('novo/', views.criar_cliente, name='criar_cliente'),
    path('editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
    path('detalhes/<int:id>/', views.detalhes_cliente, name='detalhes_cliente'),
]