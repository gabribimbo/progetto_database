from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionale', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='ruolo_operativo',
            new_name='ruolo',
        ),
    ]
