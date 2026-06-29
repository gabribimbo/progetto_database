import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServizioPulizia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120)),
                ('descrizione', models.TextField()),
                ('prezzo_base', models.DecimalField(decimal_places=2, max_digits=10)),
                ('durata_stimata', models.DurationField(help_text='Formato consigliato: HH:MM:SS')),
                ('tipo_servizio', models.CharField(choices=[('Ordinaria', 'Ordinaria'), ('Straordinaria', 'Straordinaria'), ('Sanificazione', 'Sanificazione')], max_length=30)),
                ('frequenza', models.CharField(blank=True, max_length=100, null=True)),
                ('livello_sporco', models.CharField(blank=True, max_length=100, null=True)),
                ('prodotto_utilizzato', models.CharField(blank=True, max_length=150, null=True)),
                ('certificazione_richiesta', models.BooleanField(default=False)),
                ('recensione', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Servizio di pulizia',
                'verbose_name_plural': 'Servizi di pulizia',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cognome', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('tipo_cliente', models.CharField(choices=[('Privato', 'Privato'), ('Azienda', 'Azienda')], max_length=20)),
                ('codice_fiscale', models.CharField(blank=True, max_length=16, null=True)),
                ('indirizzo_abitazione', models.CharField(blank=True, max_length=255, null=True)),
                ('partita_iva', models.CharField(blank=True, max_length=20, null=True)),
                ('sede_legale', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clienti',
            },
        ),
        migrations.CreateModel(
            name='ProfiloUtente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(max_length=30)),
                ('ruolo', models.CharField(choices=[('Cliente', 'Cliente'), ('Staff', 'Staff'), ('Admin', 'Admin')], default='Cliente', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profilo utente',
                'verbose_name_plural': 'Profili utente',
            },
        ),
        migrations.CreateModel(
            name='Prenotazione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantita', models.PositiveIntegerField(default=1)),
                ('data_richiesta', models.DateTimeField(auto_now_add=True)),
                ('data_servizio', models.DateTimeField()),
                ('stato', models.CharField(choices=[('In attesa', 'In attesa'), ('Confermata', 'Confermata'), ('Completata', 'Completata'), ('Annullata', 'Annullata')], default='In attesa', max_length=20)),
                ('indirizzo_intervento', models.CharField(max_length=255)),
                ('importo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('metodo_pagamento', models.CharField(blank=True, max_length=100, null=True)),
                ('data_pagamento', models.DateTimeField(blank=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prenotazioni', to='gestionale.cliente')),
                ('servizio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prenotazioni', to='gestionale.serviziopulizia')),
            ],
            options={
                'verbose_name': 'Prenotazione',
                'verbose_name_plural': 'Prenotazioni',
                'ordering': ['-data_servizio'],
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cognome', models.CharField(max_length=100)),
                ('ruolo_operativo', models.CharField(choices=[('Titolare', 'Titolare'), ('Capo area', 'Capo area'), ('Capo squadra', 'Capo squadra'), ('Operaio', 'Operaio')], max_length=20)),
                ('specializzazione', models.CharField(blank=True, max_length=150, null=True)),
                ('quota_societaria', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('area_competenza', models.CharField(blank=True, max_length=100, null=True)),
                ('numero_squadra', models.CharField(blank=True, max_length=50, null=True)),
                ('disponibilita', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Staff',
                'verbose_name_plural': 'Staff',
            },
        ),
        migrations.CreateModel(
            name='Esegue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servizio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_esecutori', to='gestionale.serviziopulizia')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servizi_eseguiti', to='gestionale.staff')),
            ],
            options={
                'verbose_name': 'Esecuzione',
                'verbose_name_plural': 'Esecuzioni',
                'unique_together': {('staff', 'servizio')},
            },
        ),
    ]
