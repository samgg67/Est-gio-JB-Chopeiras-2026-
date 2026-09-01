from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser

from clientes.models import Clientes, LocalizacaoEmpresa, PerguntaFrequente
from clientes.serializer import ClientesSerializer
from clientes.formulario import ClientesFormulario, PerfilClienteFormulario
from servicos.models import Servico


def home(request):
    return render(request, 'home.html')


def sair(request):
    logout(request)
    return redirect('home')


def tela_entrada(request):
    mensagem = None

    if request.method == 'POST':
        tipo_form = request.POST.get('tipo_form')
        email = request.POST.get('email', '').strip().lower()
        senha = request.POST.get('senha', '').strip()

        if tipo_form == 'login':
            if not email or not senha:
                mensagem = 'Preencha e-mail e senha.'
            else:
                usuario_obj = User.objects.filter(email__iexact=email).first()
                usuario = authenticate(
                    request,
                    username=usuario_obj.username if usuario_obj else '',
                    password=senha,
                )
                if usuario is None:
                    mensagem = 'Usuário ou senha inválida.'
                else:
                    login(request, usuario)
                    return redirect('servicos:lista' if usuario.is_staff else 'home')

        elif tipo_form == 'registro':
            nome = request.POST.get('nome', '').strip()
            telefone = request.POST.get('telefone', '').strip()
            endereco = request.POST.get('endereco', '').strip()
            confirmar_senha = request.POST.get('confirmar_senha', '').strip()

            if not all((nome, email, telefone, endereco, senha, confirmar_senha)):
                mensagem = 'Preencha todos os campos obrigatórios.'
            elif senha != confirmar_senha:
                mensagem = 'As senhas não coincidem.'
            elif User.objects.filter(username__iexact=email).exists():
                mensagem = 'Já existe um usuário com esse e-mail.'
            elif Clientes.objects.filter(email__iexact=email).exists():
                mensagem = 'Já existe um cliente cadastrado com esse e-mail.'
            else:
                with transaction.atomic():
                    usuario = User.objects.create_user(
                        username=email,
                        email=email,
                        password=senha,
                        first_name=nome,
                    )
                    Clientes.objects.create(
                        usuario=usuario,
                        nome=nome,
                        email=email,
                        telefone=telefone,
                        endereco=endereco,
                    )
                login(request, usuario)
                return redirect('home')

    return render(request, 'login.html', {'mensagem': mensagem})


class ClientesViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = ClientesSerializer

    def get_queryset(self):
        return Clientes.objects.all()


def duvidas(request):
    perguntas = PerguntaFrequente.objects.filter(ativa=True)
    return render(request, 'clientes/duvidas.html', {'perguntas': perguntas})


def localizacao(request):
    local = LocalizacaoEmpresa.objects.filter(ativa=True).first()
    return render(request, 'clientes/localizacao.html', {'local': local})


@login_required(login_url='tela_entrada')
def historico(request):
    email = request.user.email or request.user.username
    solicitacoes = Servico.objects.filter(
        Q(usuario=request.user) |
        Q(usuario__isnull=True, email__iexact=email)
    ).distinct()
    resumo = {
        'total': solicitacoes.count(),
        'pendentes': solicitacoes.filter(status='p').count(),
        'andamento': solicitacoes.filter(status='a').count(),
        'finalizados': solicitacoes.filter(status='f').count(),
    }

    status_selecionado = request.GET.get('status', '')
    if status_selecionado in {'p', 'a', 'f'}:
        servicos = solicitacoes.filter(status=status_selecionado)
    else:
        status_selecionado = ''
        servicos = solicitacoes

    return render(request, 'clientes/historico.html', {
        'servicos': servicos,
        'resumo': resumo,
        'status_selecionado': status_selecionado,
    })


def _obter_perfil_cliente(usuario):
    try:
        return usuario.perfil_cliente
    except Clientes.DoesNotExist:
        perfil = Clientes.objects.filter(email__iexact=usuario.email).first()
        if perfil and perfil.usuario_id is None:
            perfil.usuario = usuario
            perfil.save(update_fields=['usuario'])
        return perfil


def _bloqueio_area_administrativa(request):
    """Redireciona quem não pode acessar as páginas administrativas."""
    if not request.user.is_authenticated:
        return redirect('tela_entrada')
    if not request.user.is_staff:
        return redirect('home')
    return None


@login_required(login_url='tela_entrada')
def perfil_cliente(request):
    cliente = _obter_perfil_cliente(request.user)

    if cliente is None:
        cliente = Clientes(
            usuario=request.user,
            email=request.user.email or request.user.username,
        )

    form = PerfilClienteFormulario(request.POST or None, instance=cliente)
    sucesso = False

    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.email = request.user.email or request.user.username
            cliente.save()
            request.user.first_name = cliente.nome
            request.user.save(update_fields=['first_name'])
        sucesso = True

    return render(
        request,
        'clientes/perfil_cliente.html',
        {'form': form, 'sucesso': sucesso},
    )


@login_required(login_url='tela_entrada')
def trocar_senha(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    sucesso = False

    if request.method == 'POST' and form.is_valid():
        usuario = form.save()
        update_session_auth_hash(request, usuario)
        form = PasswordChangeForm(user=request.user)
        sucesso = True

    return render(
        request,
        'clientes/trocar_senha.html',
        {'form': form, 'sucesso': sucesso},
    )


def clientesPage(request):
    bloqueio = _bloqueio_area_administrativa(request)
    if bloqueio:
        return bloqueio

    pesquisa = request.GET.get('q', '').strip()

    clientes = Clientes.objects.all().order_by('nome')

    if pesquisa:
        clientes = clientes.filter( Q(nome__icontains=pesquisa) | Q(email__icontains=pesquisa) | Q(telefone__icontains=pesquisa) )

    paginador = Paginator(clientes, 30)
    pagina = paginador.get_page(request.GET.get('page'))

    return render(request, 'clientes/clientesPage.html', {
        'clientes': pagina,
        'pagina': pagina,
        'pesquisa': pesquisa,
    })


def criar_cliente(request):
    bloqueio = _bloqueio_area_administrativa(request)
    if bloqueio:
        return bloqueio

    if request.method == 'POST':
        form = ClientesFormulario(request.POST)

        if form.is_valid():
            form.save()
            return redirect('clientesPage')

    else:
        form = ClientesFormulario()

    return render(
        request, 'clientes/cliente_formulario.html',{ 'form': form, 'titulo': 'Criar Cliente'})


def editar_cliente(request, id):
    bloqueio = _bloqueio_area_administrativa(request)
    if bloqueio:
        return bloqueio

    cliente = get_object_or_404( Clientes, id=id)

    if request.method == 'POST':
        form = ClientesFormulario( request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            return redirect('clientesPage')

    else:
        form = ClientesFormulario( instance=cliente)

    return render(
        request, 'clientes/cliente_formulario.html',{ 'form': form,'titulo': 'Editar Cliente'})


def inativar_cliente(request, id):
    bloqueio = _bloqueio_area_administrativa(request)
    if bloqueio:
        return bloqueio

    cliente = get_object_or_404( Clientes, id=id, deletado_em__isnull=True)

    if request.method == 'POST':
        cliente.deletado_em = timezone.now()

        cliente.save( update_fields=['deletado_em'] )

        return redirect('clientesPage')

    return render( request, 'clientes/confirmar_exclusao.html', { 'cliente': cliente, 'titulo': 'Inativar Cliente' } )


def reativar_cliente(request, id):
    bloqueio = _bloqueio_area_administrativa(request)
    if bloqueio:
        return bloqueio

    cliente = get_object_or_404( Clientes, id=id )

    if request.method == 'POST':
        cliente.deletado_em = None

        cliente.save( update_fields=['deletado_em'])

        return redirect('clientesPage')

    return render( request, 'clientes/confirmar_reativacao.html', { 'cliente': cliente, 'titulo': 'Reativar Cliente' } )


def detalhes_cliente(request, id):
    bloqueio = _bloqueio_area_administrativa(request)
    if bloqueio:
        return bloqueio

    cliente = get_object_or_404( Clientes, id=id )

    return render( request,'clientes/detalhes_cliente.html', { 'cliente': cliente } )
