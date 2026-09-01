from django.contrib import admin
from django.urls import path, include
from servicos.views import ServicoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('servicos', ServicoViewSet, basename='servicos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clientes.urls_publicas')),
    path('clientes/', include('clientes.urls')),
    path('', include('JB_Chopeiras.urls')),
    path('servicos/', include('servicos.urls')),
    path('api/', include(router.urls)),
]
