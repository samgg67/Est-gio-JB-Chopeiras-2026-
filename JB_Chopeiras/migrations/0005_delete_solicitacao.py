
from django.db import migrations


def migrar_solicitacoes(apps, schema_editor):
    Solicitacao = apps.get_model('JB_Chopeiras', 'Solicitacao')
    Servico = apps.get_model('servicos', 'Servico')
    protocolo = Servico.objects.order_by('-protocolo').values_list(
        'protocolo', flat=True
    ).first() or 0

    novos_servicos = []
    for solicitacao in Solicitacao.objects.order_by('data_criacao', 'pk'):
        protocolo += 1
        status = {
            'pendente': 'p',
            'andamento': 'a',
            'finalizado': 'f',
        }.get(solicitacao.status, 'p')
        novos_servicos.append(Servico(
            protocolo=protocolo,
            nome=solicitacao.nome[:50],
            email=solicitacao.email[:50],
            telefone='',
            endereco=solicitacao.endereco[:50],
            problema=solicitacao.problema[:20],
            status=status,
            notas=solicitacao.explicacao[:250],
            criado_em=solicitacao.data_criacao,
        ))
    Servico.objects.bulk_create(novos_servicos)


class Migration(migrations.Migration):

    dependencies = [
        ('JB_Chopeiras', '0004_relatorio'),
        ('servicos', '0005_alter_servico_options_servico_criado_em_and_more'),
    ]

    operations = [
        migrations.RunPython(migrar_solicitacoes, migrations.RunPython.noop),
        migrations.DeleteModel(
            name='Solicitacao',
        ),
    ]
