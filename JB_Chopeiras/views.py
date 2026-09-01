import base64
from io import BytesIO

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth, ExtractYear
from django.shortcuts import render

from servicos.models import Servico

from .models import Relatorio


MESES = [
    (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'),
    (5, 'Maio'), (6, 'Junho'), (7, 'Julho'), (8, 'Agosto'),
    (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'),
]

NOMES_MESES = dict(MESES)
MESES_ABREVIADOS = {
    1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
    5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
    9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez',
}


def grafico_para_base64():
    """Converte o gráfico atual em uma imagem para exibir no HTML."""
    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    imagem = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()
    return imagem


def opcoes_de_periodo():
    """Retorna os meses e anos que possuem solicitações."""
    meses = (
        Servico.objects.annotate(mes=ExtractMonth('criado_em'))
        .values_list('mes', flat=True)
        .distinct()
        .order_by('mes')
    )
    anos = (
        Servico.objects.annotate(ano=ExtractYear('criado_em'))
        .values_list('ano', flat=True)
        .distinct()
        .order_by('-ano')
    )
    return meses, anos


@login_required(login_url='tela_entrada')
def relatorios(request):
    mes_selecionado = request.GET.get('mes')
    ano_selecionado = request.GET.get('ano')
    solicitacoes = Servico.objects.all()

    if mes_selecionado:
        solicitacoes = solicitacoes.filter(criado_em__month=mes_selecionado)
    if ano_selecionado:
        solicitacoes = solicitacoes.filter(criado_em__year=ano_selecionado)

    quantidade_por_mes = {}
    clientes_por_mes = {}
    for criado_em, nome in solicitacoes.values_list('criado_em', 'nome'):
        mes = criado_em.month
        quantidade_por_mes[mes] = quantidade_por_mes.get(mes, 0) + 1
        clientes_por_mes.setdefault(mes, set()).add(nome)

    grafico_servicos = None
    grafico_clientes = None

    if quantidade_por_mes:
        meses_com_dados = sorted(quantidade_por_mes)
        nomes = [MESES_ABREVIADOS[mes] for mes in meses_com_dados]

        plt.figure(figsize=(7, 4))
        plt.bar(nomes, [quantidade_por_mes[mes] for mes in meses_com_dados])
        plt.title('Serviços realizados')
        plt.xlabel('Mês')
        plt.ylabel('Quantidade')
        grafico_servicos = grafico_para_base64()

        plt.figure(figsize=(7, 4))
        plt.plot(
            nomes,
            [len(clientes_por_mes[mes]) for mes in meses_com_dados],
            marker='o',
        )
        plt.title('Total de clientes')
        plt.xlabel('Mês')
        plt.ylabel('Clientes')
        grafico_clientes = grafico_para_base64()

    meses, anos = opcoes_de_periodo()
    contexto = {
        'grafico_servicos': grafico_servicos,
        'grafico_clientes': grafico_clientes,
        'meses': meses,
        'anos': anos,
        'mes_selecionado': mes_selecionado,
        'ano_selecionado': ano_selecionado,
    }
    return render(request, 'relatorios.html', contexto)


@login_required(login_url='tela_entrada')
def gerar_relatorio(request):
    relatorio = None
    solicitacoes = None
    mes_selecionado = None
    ano_selecionado = None

    if request.method == 'POST':
        mes_selecionado = request.POST.get('mes')
        ano_selecionado = request.POST.get('ano')

        if mes_selecionado and ano_selecionado:
            solicitacoes = Servico.objects.filter(
                criado_em__month=mes_selecionado,
                criado_em__year=ano_selecionado,
            ).order_by('criado_em')

            totais = {
                'total': solicitacoes.count(),
                'pendentes': solicitacoes.filter(status='p').count(),
                'andamento': solicitacoes.filter(status='a').count(),
                'finalizados': solicitacoes.filter(status='f').count(),
                'total_clientes': solicitacoes.values('email').distinct().count(),
            }

            Relatorio.objects.update_or_create(
                mes=int(mes_selecionado),
                ano=int(ano_selecionado),
                defaults=totais,
            )

            relatorio = {
                'mes': NOMES_MESES[int(mes_selecionado)],
                'ano': ano_selecionado,
                **totais,
            }

    _, anos = opcoes_de_periodo()
    contexto = {
        'meses': MESES,
        'anos': anos,
        'relatorio': relatorio,
        'solicitacoes': solicitacoes,
        'mes_selecionado': mes_selecionado,
        'ano_selecionado': ano_selecionado,
    }
    return render(request, 'gerar_relatorio.html', contexto)


@login_required(login_url='tela_entrada')
def visualizar_relatorios(request):
    relatorios_salvos = Relatorio.objects.all().order_by('-ano', '-mes')

    for relatorio in relatorios_salvos:
        relatorio.nome_mes = NOMES_MESES.get(relatorio.mes)

    return render(
        request,
        'visualizar_relatorios.html',
        {'relatorios': relatorios_salvos},
    )


@login_required(login_url='tela_entrada')
def configuracoes(request):
    mensagem = None

    if request.method == 'POST' and request.POST.get('tipo_form') == 'senha':
        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not request.user.check_password(senha_atual):
            mensagem = 'Senha atual incorreta.'
        elif nova_senha != confirmar_senha:
            mensagem = 'As novas senhas não coincidem.'
        elif not nova_senha:
            mensagem = 'Informe uma nova senha.'
        else:
            request.user.set_password(nova_senha)
            request.user.save()
            update_session_auth_hash(request, request.user)
            mensagem = 'Senha alterada com sucesso.'

    return render(request, 'configuracoes.html', {'mensagem': mensagem})
