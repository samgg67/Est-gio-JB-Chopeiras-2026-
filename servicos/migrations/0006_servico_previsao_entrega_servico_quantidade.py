
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0005_alter_servico_options_servico_criado_em_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='previsao_entrega',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='servico',
            name='quantidade',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
