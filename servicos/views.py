from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser

from .formulario import ServicoFormulario, SolicitacaoFormulario
from .models import Servico
from .serializer import ServicoSerializer

staff_required = user_passes_test(
    lambda usuario: usuario.is_authenticated and usuario.is_staff,
    login_url='tela_entrada',
)


class ServicoViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer


@login_required(login_url='tela_entrada')
@staff_required
def dashboard(request):
    contexto = {
        'pedidos_totais': Servico.objects.count(),
        'em_atendimento': Servico.objects.filter(status='a').count(),
        'finalizados': Servico.objects.filter(status='f').count(),
        'pendentes': Servico.objects.filter(status='p').count(),
        'ultimas_solicitacoes': Servico.objects.all()[:5],
    }
    return render(request, 'servicos/dashboard.html', contexto)


@login_required(login_url='tela_entrada')
@staff_required
def lista(request):
    pesquisa = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    solicitacoes = Servico.objects.all()

    if pesquisa:
        filtros = (
            Q(nome__icontains=pesquisa) |
            Q(email__icontains=pesquisa) |
            Q(telefone__icontains=pesquisa) |
            Q(problema__icontains=pesquisa)
        )
        if pesquisa.isdigit():
            filtros |= Q(protocolo=int(pesquisa))
        solicitacoes = solicitacoes.filter(filtros)

    status_validos = {valor for valor, _ in Servico.STATUS_CHOICES}
    if status in status_validos:
        solicitacoes = solicitacoes.filter(status=status)
    else:
        status = ''

    paginador = Paginator(solicitacoes, 30)
    pagina = paginador.get_page(request.GET.get('page'))

    return render(request, 'servicos/lista.html', {
        'servicos': pagina,
        'pagina': pagina,
        'pesquisa': pesquisa,
        'status_selecionado': status,
        'total_encontrado': paginador.count,
        'status_opcoes': Servico.STATUS_CHOICES,
    })


@login_required(login_url='tela_entrada')
def solicitar(request):
    perfil = getattr(request.user, 'perfil_cliente', None)
    dados_iniciais = {
        'nome': request.user.first_name or (perfil.nome if perfil else ''),
        'telefone': perfil.telefone if perfil else '',
        'endereco': perfil.endereco if perfil else '',
    }
    form = SolicitacaoFormulario(request.POST or None, initial=dados_iniciais)
    if request.method == 'POST' and form.is_valid():
        servico = form.save(commit=False)
        servico.usuario = request.user
        servico.email = request.user.email or request.user.username
        servico.save()
        return redirect('servicos:sucesso')
    return render(request, 'servicos/solicitar.html', {'form': form})


@login_required(login_url='tela_entrada')
def sucesso(request):
    return render(request, 'servicos/sucesso.html')


@login_required(login_url='tela_entrada')
@staff_required
def criar(request):
    form = ServicoFormulario(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('servicos:lista')
    return render(request, 'servicos/formulario.html', {'form': form, 'titulo': 'Criar solicitação'})


@login_required(login_url='tela_entrada')
@staff_required
def editar(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    form = ServicoFormulario(request.POST or None, instance=servico)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('servicos:lista')
    return render(request, 'servicos/formulario.html', {'form': form, 'titulo': 'Editar solicitação'})


@login_required(login_url='tela_entrada')
@staff_required
def excluir(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        servico.delete()
        return redirect('servicos:lista')
    return render(request, 'servicos/confirmar_exclusao.html', {'servico': servico})
