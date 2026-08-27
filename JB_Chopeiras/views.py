from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth, ExtractYear

from .forms import SolicitacaoForm
from clientes.models import Clientes
from .models import Solicitacao, Relatorio

import pandas as pd

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import base64
from io import BytesIO


def home(request):
    return render(request, 'home.html')



def sair(request):
    logout(request)
    return redirect('home')

#----------------------------------------------------------------------------------------------------------------------
    

def tela_entrada(request):

    mensagem = None

    if request.method == 'POST':

        tipo_form = request.POST.get('tipo_form')

        if tipo_form == 'login':

            email = request.POST.get('email', '').strip()
            senha = request.POST.get('senha', '').strip()

            if not email or not senha:

                mensagem = 'Preencha email e senha.'

            else:

                try:

                    usuario_obj = User.objects.get(email=email)

                    usuario = authenticate(request, username=usuario_obj.username, password=senha)

                    if usuario is not None:

                        login(request, usuario)

                        return redirect( 'servicosPage'
                            if usuario.is_staff
                            else 'home'
                        )

                    else:

                        mensagem = 'Usuário ou senha inválida.'

                except User.DoesNotExist:

                    mensagem = 'Usuário ou senha inválida.'

        elif tipo_form == 'registro':

            nome = request.POST.get('nome','').strip()

            email = request.POST.get('email','').strip()

            telefone = request.POST.get('telefone','').strip()

            endereco = request.POST.get('endereco', '').strip()

            senha = request.POST.get( 'senha', '').strip()

            confirmar_senha = request.POST.get( 'confirmar_senha','' ).strip()

            if (
                not nome
                or not email
                or not telefone
                or not endereco
                or not senha
                or not confirmar_senha
            ):

                mensagem = ( 'Preencha todos os campos obrigatórios.')

            elif senha != confirmar_senha:

                mensagem = 'As senhas não coincidem.'

            elif User.objects.filter( username=email ).exists():

                mensagem = ( 'Já existe um usuário com esse email.')

            elif Clientes.objects.filter(  email=email).exists():

                mensagem = ( 'Já existe um cliente cadastrado ' 'com esse email.')

            else:

                usuario = User.objects.create_user( username=email, email=email, password=senha)

                Clientes.objects.create( nome=nome, email=email, telefone=telefone, endereco=endereco, tempo_de_fidelidade=0, servicos_realizados=0, deletado_em=None)

                login(request, usuario)

                return redirect('home')

    return render(request, 'login.html',{'mensagem': mensagem})

#--------------------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='tela_entrada')
def preencher_formulario(request):

    if request.method == 'POST':

        form = SolicitacaoForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('formulario_sucesso')

    else:

        form = SolicitacaoForm()

    return render(request, 'formulario.html',{'form': form})

# --------------------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='tela_entrada')
def formulario_sucesso(request):

    return render(request, 'formulario_sucesso.html')


# --------------------------------------------------------------------------------------------------------------------------------------


@login_required(login_url='tela_entrada')
def dashboard(request):

    return render(request, 'dashboard.html')


# --------------------------------------------------------------------------------------------------------------------------------------

def grafico_para_base64():

    buffer = BytesIO()

    plt.tight_layout()

    plt.savefig(buffer, format='png', bbox_inches='tight')

    buffer.seek(0)

    imagem = base64.b64encode( buffer.getvalue()).decode('utf-8')

    buffer.close()

    plt.close()

    return imagem


# --------------------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='tela_entrada')
def relatorios(request):

    mes_selecionado = request.GET.get('mes')
    ano_selecionado = request.GET.get('ano')

    solicitacoes = Solicitacao.objects.all()

    anos = (Solicitacao.objects .annotate(ano=ExtractYear('data_criacao')) .values_list('ano', flat=True) .distinct() .order_by('-ano'))

    meses = (Solicitacao.objects .annotate(mes=ExtractMonth('data_criacao')) .values_list('mes', flat=True) .distinct() .order_by('mes'))

    if mes_selecionado: solicitacoes = solicitacoes.filter(data_criacao__month=mes_selecionado)

    if ano_selecionado: solicitacoes = solicitacoes.filter(data_criacao__year=ano_selecionado)

    dados = []

    for solicitacao in solicitacoes:
        dados.append(
            {
                'mes': solicitacao.data_criacao.month,
                'ano': solicitacao.data_criacao.year,
                'cliente': solicitacao.nome
            }
        )

    df = pd.DataFrame(dados)

    grafico_servicos = None
    grafico_clientes = None

    if not df.empty:
        nomes_meses = {
            1: 'Jan',
            2: 'Fev',
            3: 'Mar',
            4: 'Abr',
            5: 'Mai',
            6: 'Jun',
            7: 'Jul',
            8: 'Ago',
            9: 'Set',
            10: 'Out',
            11: 'Nov',
            12: 'Dez'
        }

        servicos_mes = (df.groupby('mes') .size() .reset_index(name='quantidade'))

        servicos_mes['nome_mes'] = (servicos_mes['mes'] .map(nomes_meses))

        plt.figure(figsize=(7, 4))

        plt.bar(servicos_mes['nome_mes'], servicos_mes['quantidade'])

        plt.title('Serviços realizados')

        plt.xlabel('Mês')

        plt.ylabel('Quantidade')

        grafico_servicos = (grafico_para_base64())

        clientes_mes = (df.groupby('mes')['cliente'] .nunique() .reset_index(name='clientes'))

        clientes_mes['nome_mes'] = (clientes_mes['mes'] .map(nomes_meses))

        plt.figure( figsize=(7, 4))

        plt.plot( clientes_mes['nome_mes'], clientes_mes['clientes'], marker='o' )

        plt.title('Total de clientes')

        plt.xlabel('Mês')

        plt.ylabel('Clientes')

        grafico_clientes = (grafico_para_base64())

    contexto = {
        'grafico_servicos': grafico_servicos,
        'grafico_clientes': grafico_clientes,
        'meses': meses,
        'anos': anos,
        'mes_selecionado': mes_selecionado,
        'ano_selecionado': ano_selecionado
    }

    return render(
        request,
        'relatorios.html',
        contexto
    )


# --------------------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='tela_entrada')
def gerar_relatorio(request):

    relatorio = None
    solicitacoes = None

    meses = [
        (1, 'Janeiro'),
        (2, 'Fevereiro'),
        (3, 'Março'),
        (4, 'Abril'),
        (5, 'Maio'),
        (6, 'Junho'),
        (7, 'Julho'),
        (8, 'Agosto'),
        (9, 'Setembro'),
        (10, 'Outubro'),
        (11, 'Novembro'),
        (12, 'Dezembro'),
    ]

    anos = (
        Solicitacao.objects
        .annotate(
            ano=ExtractYear('data_criacao')
        )
        .values_list(
            'ano',
            flat=True
        )
        .distinct()
        .order_by('-ano')
    )

    mes_selecionado = None
    ano_selecionado = None

    if request.method == 'POST':

        mes_selecionado = request.POST.get('mes')
        ano_selecionado = request.POST.get('ano')

        if mes_selecionado and ano_selecionado:

            solicitacoes = (
                Solicitacao.objects
                .filter(
                    data_criacao__month=mes_selecionado,
                    data_criacao__year=ano_selecionado
                )
                .order_by('data_criacao')
            )

            total = solicitacoes.count()

            pendentes = solicitacoes.filter(
                status='pendente'
            ).count()

            andamento = solicitacoes.filter(
                status='andamento'
            ).count()

            finalizados = solicitacoes.filter(
                status='finalizado'
            ).count()

            total_clientes = (
                solicitacoes
                .values('email')
                .distinct()
                .count()
            )

            Relatorio.objects.update_or_create(
                mes=int(mes_selecionado),
                ano=int(ano_selecionado),
                defaults={
                    'total': total,
                    'pendentes': pendentes,
                    'andamento': andamento,
                    'finalizados': finalizados,
                    'total_clientes': total_clientes,
                }
            )

            nome_mes = dict(meses).get(
                int(mes_selecionado)
            )

            relatorio = {
                'mes': nome_mes,
                'ano': ano_selecionado,
                'total': total,
                'pendentes': pendentes,
                'andamento': andamento,
                'finalizados': finalizados,
                'total_clientes': total_clientes,
            }

    contexto = {
        'meses': meses,
        'anos': anos,
        'relatorio': relatorio,
        'solicitacoes': solicitacoes,
        'mes_selecionado': mes_selecionado,
        'ano_selecionado': ano_selecionado,
    }

    return render(
        request,
        'gerar_relatorio.html',
        contexto
    )

#--------------------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='tela_entrada')
def visualizar_relatorios(request):

    relatorios_salvos = Relatorio.objects.all().order_by(
        '-ano',
        '-mes'
    )

    nomes_meses = {
        1: 'Janeiro',
        2: 'Fevereiro',
        3: 'Março',
        4: 'Abril',
        5: 'Maio',
        6: 'Junho',
        7: 'Julho',
        8: 'Agosto',
        9: 'Setembro',
        10: 'Outubro',
        11: 'Novembro',
        12: 'Dezembro',
    }

    for relatorio in relatorios_salvos:

        relatorio.nome_mes = nomes_meses.get(
            relatorio.mes
        )

    return render(
        request,
        'visualizar_relatorios.html',
        {
            'relatorios': relatorios_salvos
        }
    )

#--------------------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='tela_entrada')
def configuracoes(request):

    mensagem = None

    if request.method == 'POST':

        tipo_form = request.POST.get('tipo_form')

        if tipo_form == 'senha':

            senha_atual = request.POST.get(
                'senha_atual'
            )

            nova_senha = request.POST.get(
                'nova_senha'
            )

            confirmar_senha = request.POST.get(
                'confirmar_senha'
            )

            if not request.user.check_password(
                senha_atual
            ):
                mensagem = 'Senha atual incorreta.'

            elif nova_senha != confirmar_senha:

                mensagem = (
                    'As novas senhas não coincidem.'
                )

            elif not nova_senha:

                mensagem = (
                    'Informe uma nova senha.'
                )

            else:

                request.user.set_password(
                    nova_senha
                )

                request.user.save()

                login(
                    request,
                    request.user
                )

                mensagem = (
                    'Senha alterada com sucesso.'
                )

    return render(
        request,
        'configuracoes.html',
        {
            'mensagem': mensagem
        }
    )