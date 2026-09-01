from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0009_localizacaoempresa'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='clientes',
            table='clientes',
        ),
        migrations.AlterModelTable(
            name='localizacaoempresa',
            table='localizacoes',
        ),
        migrations.AlterModelTable(
            name='perguntafrequente',
            table='perguntas_frequentes',
        ),
    ]
