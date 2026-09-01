from django.db import migrations, models


def criar_localizacao_inicial(apps, schema_editor):
    LocalizacaoEmpresa = apps.get_model('clientes', 'LocalizacaoEmpresa')
    LocalizacaoEmpresa.objects.create(
        nome='JB Chopeiras',
        endereco='Av. São João, 2935',
        cidade='Londrina',
        estado='PR',
        telefone='(43) 98402-2769',
        horario_atendimento='Segunda a sexta, das 8h às 18h',
        url_mapa='https://www.google.com/maps?q=Av.+S%C3%A3o+Jo%C3%A3o,+2935,+Aritana,+Londrina,+PR&output=embed',
        numero_whatsapp='5543984022769',
        ativa=True,
    )


class Migration(migrations.Migration):
    dependencies = [('clientes', '0008_clientes_usuario')]

    operations = [
        migrations.CreateModel(
            name='LocalizacaoEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='JB Chopeiras', max_length=100)),
                ('endereco', models.CharField(max_length=180)),
                ('cidade', models.CharField(default='Londrina', max_length=80)),
                ('estado', models.CharField(default='PR', max_length=2)),
                ('cep', models.CharField(blank=True, max_length=9)),
                ('telefone', models.CharField(max_length=20)),
                ('horario_atendimento', models.CharField(max_length=150)),
                ('url_mapa', models.URLField(max_length=500)),
                ('numero_whatsapp', models.CharField(help_text='Somente números, incluindo código do país e DDD.', max_length=20)),
                ('ativa', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'localização da empresa',
                'verbose_name_plural': 'localizações da empresa',
            },
        ),
        migrations.RunPython(criar_localizacao_inicial, migrations.RunPython.noop),
    ]
