
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='endereco',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='servico',
            name='telefone',
            field=models.CharField(max_length=20),
        ),
    ]
