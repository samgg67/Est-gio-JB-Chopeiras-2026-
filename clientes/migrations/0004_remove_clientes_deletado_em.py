
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0003_clientes_deletado_em'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientes',
            name='deletado_em',
        ),
    ]
