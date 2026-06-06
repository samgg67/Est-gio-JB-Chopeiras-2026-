from django.shortcuts import render
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser

from clientes.models import Clientes
from clientes.serializer import ClientesSerializer
from clientes.formulario import ClientesFormulario


class ClientesViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer

def clientesPage(request):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    if not request.user.is_staff:
        return redirect('home')

    pesquisa = request.GET.get('q', '')

    clientes = Clientes.objects.all()

    if pesquisa:
        clientes = clientes.filter(
            Q(nome__icontains=pesquisa)
        )

    return render(
        request,
        'clientes/clientesPage.html',
        {
            'clientes': clientes,
            'pesquisa': pesquisa
        }
    )

def criar_cliente(request):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        form = ClientesFormulario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientesPage')
    else:
        form = ClientesFormulario()

    return render(request, 'clientes/cliente_formulario.html', {'form': form,'titulo': 'Criar Cliente'})

def editar_cliente(request, id):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    if not request.user.is_staff:
        return redirect('home')

    cliente = get_object_or_404(Clientes, id=id)

    if request.method == 'POST':
        form = ClientesFormulario(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientesPage')
    else:
        form = ClientesFormulario(instance=cliente)

    return render(request, 'clientes/cliente_formulario.html', {
    'form': form,
    'titulo': 'Editar Cliente'
    })

def excluir_cliente(request, id):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    if not request.user.is_staff:
        return redirect('home')

    cliente = get_object_or_404(Clientes, id=id)

    if request.method == 'POST':
        cliente.delete()
        return redirect('clientesPage')

    return render(request, 'clientes/confirmar_exclusao.html', {
        'cliente': cliente,
        'titulo': 'Excluir Cliente'
    })

def detalhes_cliente(request, id):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    cliente = get_object_or_404(Clientes, id=id)

    return render(
        request,
        'clientes/detalhes_cliente.html',
        {'cliente': cliente}
    )

