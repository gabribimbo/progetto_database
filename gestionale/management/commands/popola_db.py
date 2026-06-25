from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from gestionale.models import (
    Cliente,
    Esegue,
    Prenotazione,
    ProfiloUtente,
    Prodotto,
    ServizioPulizia,
    Squadra,
    Staff,
)


class Command(BaseCommand):
    help = "Popola il database con dati iniziali per provare l'applicazione."

    def handle(self, *args, **options):
        admin_user = self.get_or_create_user("admin_demo", "admin@example.com", "Admin", "Demo", True, True)
        cliente_user = self.get_or_create_user("cliente_demo", "cliente@example.com", "Mario", "Rossi", False, False)
        azienda_user = self.get_or_create_user("azienda_demo", "azienda@example.com", "Laura", "Bianchi", False, False)
        titolare_user = self.get_or_create_user("titolare_demo", "titolare@example.com", "Roberto", "Marini", True, False)
        capo_area_user = self.get_or_create_user("capo_area_demo", "capoarea@example.com", "Elena", "Fontana", True, False)
        staff_user = self.get_or_create_user("staff_demo", "staff@example.com", "Giulia", "Verdi", True, False)
        staff_user_2 = self.get_or_create_user("staff_demo_2", "staff2@example.com", "Paolo", "Neri", True, False)

        ProfiloUtente.objects.update_or_create(
            user=admin_user,
            defaults={"telefono": "3330000001", "ruolo": ProfiloUtente.RUOLO_ADMIN},
        )
        ProfiloUtente.objects.update_or_create(
            user=cliente_user,
            defaults={"telefono": "3330000002", "ruolo": ProfiloUtente.RUOLO_CLIENTE},
        )
        ProfiloUtente.objects.update_or_create(
            user=azienda_user,
            defaults={"telefono": "3330000003", "ruolo": ProfiloUtente.RUOLO_CLIENTE},
        )
        ProfiloUtente.objects.update_or_create(
            user=titolare_user,
            defaults={"telefono": "3330000004", "ruolo": ProfiloUtente.RUOLO_STAFF},
        )
        ProfiloUtente.objects.update_or_create(
            user=capo_area_user,
            defaults={"telefono": "3330000005", "ruolo": ProfiloUtente.RUOLO_STAFF},
        )
        ProfiloUtente.objects.update_or_create(
            user=staff_user,
            defaults={"telefono": "3330000006", "ruolo": ProfiloUtente.RUOLO_STAFF},
        )
        ProfiloUtente.objects.update_or_create(
            user=staff_user_2,
            defaults={"telefono": "3330000007", "ruolo": ProfiloUtente.RUOLO_STAFF},
        )

        cliente_privato, _ = Cliente.objects.update_or_create(
            user=cliente_user,
            defaults={
                "nome": "Mario",
                "cognome": "Rossi",
                "telefono": "3330000002",
                "email": "cliente@example.com",
                "tipo_cliente": Cliente.TIPO_PRIVATO,
                "codice_fiscale": "RSSMRA80A01H501U",
                "indirizzo_abitazione": "Via Roma 10, Milano",
            },
        )
        Cliente.objects.update_or_create(
            user=azienda_user,
            defaults={
                "nome": "Laura",
                "cognome": "Bianchi",
                "telefono": "3330000003",
                "email": "azienda@example.com",
                "tipo_cliente": Cliente.TIPO_AZIENDA,
                "partita_iva": "12345678901",
                "sede_legale": "Corso Italia 25, Torino",
            },
        )

        titolare, _ = Staff.objects.update_or_create(
            user=titolare_user,
            defaults={
                "nome": "Roberto",
                "cognome": "Marini",
                "ruolo": Staff.RUOLO_TITOLARE,
                "quota_societaria": Decimal("50.00"),
                "disponibilita": True,
            },
        )
        capo_area, _ = Staff.objects.update_or_create(
            user=capo_area_user,
            defaults={
                "nome": "Elena",
                "cognome": "Fontana",
                "ruolo": Staff.RUOLO_CAPO_AREA,
                "area_competenza": "Nord Milano",
                "disponibilita": True,
            },
        )
        staff_1, _ = Staff.objects.update_or_create(
            user=staff_user,
            defaults={
                "nome": "Giulia",
                "cognome": "Verdi",
                "ruolo": Staff.RUOLO_CAPO_SQUADRA,
                "numero_squadra": "SQ-01",
                "disponibilita": True,
            },
        )
        staff_2, _ = Staff.objects.update_or_create(
            user=staff_user_2,
            defaults={
                "nome": "Paolo",
                "cognome": "Neri",
                "ruolo": Staff.RUOLO_OPERAIO,
                "specializzazione": "Sanificazione",
                "disponibilita": True,
            },
        )

        servizio_ordinario, _ = ServizioPulizia.objects.update_or_create(
            nome="Pulizia ordinaria appartamento",
            defaults={
                "descrizione": "Pulizia completa di ambienti domestici, superfici e pavimenti.",
                "prezzo_base": Decimal("65.00"),
                "durata_stimata": timedelta(hours=2),
                "tipo_servizio": ServizioPulizia.TIPO_ORDINARIA,
                "frequenza": "Settimanale",
            },
        )
        servizio_straordinario, _ = ServizioPulizia.objects.update_or_create(
            nome="Pulizia straordinaria ufficio",
            defaults={
                "descrizione": "Intervento approfondito per uffici, sale riunioni e aree comuni.",
                "prezzo_base": Decimal("180.00"),
                "durata_stimata": timedelta(hours=5),
                "tipo_servizio": ServizioPulizia.TIPO_STRAORDINARIA,
                "livello_sporco": "Alto",
            },
        )
        servizio_sanificazione, _ = ServizioPulizia.objects.update_or_create(
            nome="Sanificazione ambienti",
            defaults={
                "descrizione": "Sanificazione con prodotti professionali e rilascio documentazione.",
                "prezzo_base": Decimal("240.00"),
                "durata_stimata": timedelta(hours=4),
                "tipo_servizio": ServizioPulizia.TIPO_SANIFICAZIONE,
                "prodotto_utilizzato": "Disinfettante professionale",
                "certificazione_richiesta": True,
            },
        )

        self.update_or_create_prenotazione(
            cliente=cliente_privato,
            servizio=servizio_ordinario,
            quantita=1,
            indirizzo_intervento="Via Roma 10, Milano",
            data_servizio=timezone.now() + timedelta(days=3),
            stato=Prenotazione.STATO_CONFERMATA,
        )
        self.update_or_create_prenotazione(
            cliente=cliente_privato,
            servizio=servizio_straordinario,
            quantita=1,
            indirizzo_intervento="Corso Italia 25, Torino",
            data_servizio=timezone.now() + timedelta(days=7),
            stato=Prenotazione.STATO_IN_ATTESA,
        )

        Esegue.objects.update_or_create(staff=staff_1, servizio=servizio_ordinario)
        Esegue.objects.update_or_create(staff=staff_2, servizio=servizio_sanificazione)
        Esegue.objects.update_or_create(staff=capo_area, servizio=servizio_straordinario)

        squadra_centro, _ = Squadra.objects.update_or_create(
            nome_squadra="Squadra Centro",
            defaults={"zona_operativa": "Centro Milano"},
        )
        squadra_nord, _ = Squadra.objects.update_or_create(
            nome_squadra="Squadra Nord",
            defaults={"zona_operativa": "Nord Milano"},
        )
        squadra_centro.composta_da.set([staff_1, staff_2])
        squadra_nord.composta_da.set([capo_area])

        prodotto_multiuso, _ = Prodotto.objects.update_or_create(
            nome_prodotto="Detergente multiuso",
            defaults={"tipo_prodotto": "Detergente"},
        )
        prodotto_disinfettante, _ = Prodotto.objects.update_or_create(
            nome_prodotto="Disinfettante professionale",
            defaults={"tipo_prodotto": "Disinfettante"},
        )
        prodotto_multiuso.utilizza.set([servizio_ordinario, servizio_straordinario])
        prodotto_disinfettante.utilizza.set([servizio_sanificazione])

        self.stdout.write(self.style.SUCCESS("Database popolato correttamente."))
        self.stdout.write(
            "Utenti demo: admin_demo, cliente_demo, azienda_demo, titolare_demo, capo_area_demo, staff_demo, staff_demo_2"
        )
        self.stdout.write("Password per tutti gli utenti demo: Password123!")

    def get_or_create_user(self, username, email, first_name, last_name, is_staff, is_superuser):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "is_staff": is_staff,
                "is_superuser": is_superuser,
            },
        )
        if created:
            user.set_password("Password123!")
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user

    def update_or_create_prenotazione(self, cliente, servizio, quantita, indirizzo_intervento, data_servizio, stato):
        prenotazione, _ = Prenotazione.objects.update_or_create(
            cliente=cliente,
            servizio=servizio,
            quantita=quantita,
            indirizzo_intervento=indirizzo_intervento,
            data_servizio=data_servizio,
            defaults={"stato": stato},
        )
        return prenotazione
