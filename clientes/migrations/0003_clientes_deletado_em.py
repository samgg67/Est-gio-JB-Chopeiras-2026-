
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_alter_clientes_endereco_alter_clientes_telefone'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='deletado_em',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
