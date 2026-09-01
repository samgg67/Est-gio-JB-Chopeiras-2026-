from django.db import migrations


def criar_perguntas_iniciais(apps, schema_editor):
    PerguntaFrequente = apps.get_model('clientes', 'PerguntaFrequente')
    perguntas = [
        ('Como entrar em contato?', 'Você pode entrar em contato pelo WhatsApp, telefone ou e-mail informados nesta página.'),
        ('Quais são as formas de pagamento?', 'As formas de pagamento disponíveis são informadas no momento do orçamento.'),
        ('Quais serviços são oferecidos?', 'Oferecemos manutenção preventiva e corretiva, instalação e higienização de chopeiras.'),
        ('Onde estamos localizados?', 'Estamos na Avenida São João, 2935, Aritana, Londrina - PR.'),
    ]
    PerguntaFrequente.objects.bulk_create([
        PerguntaFrequente(pergunta=pergunta, resposta=resposta, ordem=ordem)
        for ordem, (pergunta, resposta) in enumerate(perguntas, start=1)
    ])


def remover_perguntas_iniciais(apps, schema_editor):
    PerguntaFrequente = apps.get_model('clientes', 'PerguntaFrequente')
    PerguntaFrequente.objects.filter(
        pergunta__in=['Como entrar em contato?', 'Quais são as formas de pagamento?', 'Quais serviços são oferecidos?', 'Onde estamos localizados?']
    ).delete()


class Migration(migrations.Migration):
    dependencies = [('clientes', '0006_perguntafrequente')]
    operations = [migrations.RunPython(criar_perguntas_iniciais, remover_perguntas_iniciais)]
