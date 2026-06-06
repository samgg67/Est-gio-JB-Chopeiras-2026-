from django.urls import path
from . import views

urlpatterns = [
    path('servicos/', views.servicosPage, name='servicosPage'),
    path('servicos/novo/', views.criar_servico, name='criar_servico'),
    path('servicos/editar/<int:id>/', views.editar_servico, name='editar_servico'),
    path('servicos/excluir/<int:id>/', views.excluir_servico, name='excluir_servico'),
]