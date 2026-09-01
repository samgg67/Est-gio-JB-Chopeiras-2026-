
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='endereco',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='telefone',
            field=models.CharField(max_length=20),
        ),
    ]
