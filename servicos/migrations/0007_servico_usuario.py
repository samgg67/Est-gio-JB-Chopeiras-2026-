from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def associar_solicitacoes(apps, schema_editor):
    Servico = apps.get_model('servicos', 'Servico')
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))

    for servico in Servico.objects.filter(usuario__isnull=True):
        usuario = User.objects.filter(email__iexact=servico.email).first()
        if usuario:
            servico.usuario = usuario
            servico.save(update_fields=['usuario'])


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('servicos', '0006_servico_previsao_entrega_servico_quantidade'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='usuario',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='solicitacoes',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(associar_solicitacoes, migrations.RunPython.noop),
    ]
