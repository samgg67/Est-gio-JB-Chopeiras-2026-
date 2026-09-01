from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('JB_Chopeiras', '0005_delete_solicitacao'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='relatorio',
            table='relatorios',
        ),
    ]
