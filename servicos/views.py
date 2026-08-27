from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser

from servicos.models import Servico
from servicos.serializer import ServicoSerializer
from servicos.formulario import ServicoFormulario

staff_required = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff,
    login_url='tela_entrada'
)

class ServicoViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer

@login_required(login_url='tela_entrada')
@staff_required
def dashboard(request):

    pedidos_totais = Servico.objects.count()

    em_atendimento = Servico.objects.filter( status='a' ).count()

    finalizados = Servico.objects.filter( status='f' ).count()

    pendentes = Servico.objects.filter( status='p' ).count()

    ultimas_solicitacoes = Servico.objects.all().order_by( '-protocolo' )[:5]

    return render( request, 'dashboard.html', { 'pedidos_totais': pedidos_totais, 'em_atendimento': em_atendimento, 'finalizados': finalizados, 'pendentes': pendentes, 'ultimas_solicitacoes': ultimas_solicitacoes, } )

@login_required(login_url='tela_entrada')
@staff_required
def servicosPage(request):

    servicos = Servico.objects.all().order_by( '-protocolo' )

    return render( request, 'servicosPage.html', { 'servicos': servicos } )

@login_required(login_url='tela_entrada')
@staff_required
def criar_servico(request):

    if request.method == 'POST':

        form = ServicoFormulario( request.POST )

        if form.is_valid():

            form.save()

            return redirect( 'servicosPage' )

    else:

        form = ServicoFormulario()

    return render( request, 'servico_formulario.html', { 'form': form, 'titulo': 'Criar Solicitação' } )

@login_required(login_url='tela_entrada')
@staff_required
def editar_servico(request, id):

    servico = get_object_or_404( Servico, id=id )

    if request.method == 'POST':

        form = ServicoFormulario( request.POST, instance=servico )

        if form.is_valid():

            form.save()

            return redirect( 'servicosPage' )

    else:

        form = ServicoFormulario( instance=servico )

    return render( request, 'servico_formulario.html', { 'form': form, 'titulo': 'Editar Solicitação' } )

@login_required(login_url='tela_entrada')
@staff_required
def excluir_servico(request, id):

    servico = get_object_or_404( Servico, id=id )

    if request.method == 'POST':

        servico.delete()

        return redirect( 'servicosPage' )

    return render( request, 'servico_confirmar_exclusao.html', { 'servico': servico } )


