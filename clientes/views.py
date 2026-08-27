from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser

from clientes.models import Clientes
from clientes.serializer import ClientesSerializer
from clientes.formulario import ClientesFormulario


class ClientesViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ClientesSerializer

    def get_queryset(self):
        return Clientes.objects.all()


def clientesPage(request):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    if not request.user.is_staff:
        return redirect('home')

    pesquisa = request.GET.get('q', '').strip()

    clientes = Clientes.objects.all().order_by('nome')

    if pesquisa:
        clientes = clientes.filter( Q(nome__icontains=pesquisa) | Q(email__icontains=pesquisa) | Q(telefone__icontains=pesquisa) )

    return render( request, 'clientes/clientesPage.html', { 'clientes': clientes, 'pesquisa': pesquisa} )


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

            print('ERROS AO CRIAR CLIENTE:')
            print(form.errors)

    else:
        form = ClientesFormulario()

    return render(
        request, 'clientes/cliente_formulario.html',{ 'form': form, 'titulo': 'Criar Cliente'})


def editar_cliente(request, id):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    if not request.user.is_staff:
        return redirect('home')

    cliente = get_object_or_404( Clientes, id=id)

    if request.method == 'POST':
        form = ClientesFormulario( request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            return redirect('clientesPage')

        else:
            
            print('ERROS AO EDITAR CLIENTE:')
            print(form.errors)

    else:
        form = ClientesFormulario( instance=cliente)

    return render(
        request, 'clientes/cliente_formulario.html',{ 'form': form,'titulo': 'Editar Cliente'})


def inativar_cliente(request, id):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    if not request.user.is_staff:
        return redirect('home')

    cliente = get_object_or_404( Clientes, id=id, deletado_em__isnull=True)

    if request.method == 'POST':
        cliente.deletado_em = timezone.now()

        cliente.save( update_fields=['deletado_em'] )

        return redirect('clientesPage')

    return render( request, 'clientes/confirmar_exclusao.html', { 'cliente': cliente, 'titulo': 'Inativar Cliente' } )


def reativar_cliente(request, id):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    if not request.user.is_staff:
        return redirect('home')

    cliente = get_object_or_404( Clientes, id=id )

    if request.method == 'POST':
        cliente.deletado_em = None

        cliente.save( update_fields=['deletado_em'])

        return redirect('clientesPage')

    return render( request, 'clientes/confirmar_reativacao.html', { 'cliente': cliente, 'titulo': 'Reativar Cliente' } )


def detalhes_cliente(request, id):
    if not request.user.is_authenticated:
        return redirect('tela_entrada')

    if not request.user.is_staff:
        return redirect('home')

    cliente = get_object_or_404( Clientes, id=id )

    return render( request,'clientes/detalhes_cliente.html', { 'cliente': cliente } )