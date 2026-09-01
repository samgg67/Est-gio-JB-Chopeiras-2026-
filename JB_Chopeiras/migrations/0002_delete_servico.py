
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('JB_Chopeiras', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Servico',
        ),
    ]
