
import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicos', '0004_alter_servico_telefone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='servico',
            options={'ordering': ['-protocolo']},
        ),
        migrations.AddField(
            model_name='servico',
            name='criado_em',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='servico',
            name='nome',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[A-Za-zÀ-ÿ\\s]+$', 'O nome deve conter apenas letras e espaços.')]),
        ),
        migrations.AlterField(
            model_name='servico',
            name='status',
            field=models.CharField(choices=[('p', 'Pendente'), ('a', 'Em andamento'), ('f', 'Finalizado')], default='p', max_length=1),
        ),
        migrations.AlterField(
            model_name='servico',
            name='telefone',
            field=models.CharField(blank=True, default='', max_length=20, validators=[django.core.validators.RegexValidator('^\\d+$', 'O telefone deve conter apenas números.')]),
        ),
    ]
