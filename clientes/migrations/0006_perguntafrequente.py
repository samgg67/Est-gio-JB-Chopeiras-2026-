
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0005_clientes_deletado_em_alter_clientes_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerguntaFrequente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pergunta', models.CharField(max_length=200)),
                ('resposta', models.TextField()),
                ('ordem', models.PositiveIntegerField(default=0)),
                ('ativa', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'pergunta frequente',
                'verbose_name_plural': 'perguntas frequentes',
                'ordering': ['ordem', 'id'],
            },
        ),
    ]
