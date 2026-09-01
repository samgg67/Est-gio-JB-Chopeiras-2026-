from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0007_servico_usuario'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='servico',
            table='servicos',
        ),
    ]
