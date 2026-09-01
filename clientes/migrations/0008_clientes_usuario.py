from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def associar_usuarios(apps, schema_editor):
    Cliente = apps.get_model('clientes', 'Clientes')
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))

    for cliente in Cliente.objects.filter(usuario__isnull=True):
        usuario = User.objects.filter(email__iexact=cliente.email).first()
        if usuario and not Cliente.objects.filter(usuario=usuario).exists():
            cliente.usuario = usuario
            cliente.save(update_fields=['usuario'])


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clientes', '0007_perguntas_iniciais'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='usuario',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='perfil_cliente',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(associar_usuarios, migrations.RunPython.noop),
    ]
