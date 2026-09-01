
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JB_Chopeiras', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.PositiveIntegerField()),
                ('ano', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField(default=0)),
                ('pendentes', models.PositiveIntegerField(default=0)),
                ('andamento', models.PositiveIntegerField(default=0)),
                ('finalizados', models.PositiveIntegerField(default=0)),
                ('total_clientes', models.PositiveIntegerField(default=0)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
