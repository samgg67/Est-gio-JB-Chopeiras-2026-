
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('JB_Chopeiras', '0002_delete_servico'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('problema', models.CharField(max_length=200)),
                ('endereco', models.CharField(max_length=255)),
                ('explicacao', models.TextField()),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('andamento', 'Em andamento'), ('finalizado', 'Finalizado')], default='pendente', max_length=20)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
