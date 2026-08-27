from django.urls import path
from . import views


urlpatterns = [
    path('',views.servicosPage,name='servicosPage'),
    path('novo/',views.criar_servico,name='criar_servico'),
    path('editar/<int:id>/',views.editar_servico,name='editar_servico'),
    path('excluir/<int:id>/',views.excluir_servico,name='excluir_servico'),

]