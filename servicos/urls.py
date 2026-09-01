from django.urls import path

from . import views

app_name = 'servicos'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('solicitar/', views.solicitar, name='solicitar'),
    path('solicitar/sucesso/', views.sucesso, name='sucesso'),
    path('novo/', views.criar, name='criar'),
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/excluir/', views.excluir, name='excluir'),
]

