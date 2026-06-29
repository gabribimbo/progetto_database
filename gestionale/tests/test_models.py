from django.test import TestCase
from django.contrib.auth.models import User
from gestionale.models import Cliente, Staff, ServizioPulizia, Prenotazione, Esegue
from decimal import Decimal
from django.db import IntegrityError
import datetime


class ModelsBasicTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="u1", password="pass")
        self.user2 = User.objects.create_user(username="u2", password="pass")
        self.cliente = Cliente.objects.create(user=self.user1, nome="Mario", cognome="Rossi", telefono="123", email="m@e.it", tipo_cliente="Privato")
        self.servizio = ServizioPulizia.objects.create(
            nome="Pulizia base",
            descrizione="",
            prezzo_base=Decimal("10.00"),
            durata_stimata=datetime.timedelta(hours=1),
            tipo_servizio="Ordinaria",
        )
        self.staff = Staff.objects.create(user=self.user2, nome="Luigi", cognome="Bianchi", ruolo="Operaio")

    def test_prenotazione_totale(self):
        p = Prenotazione.objects.create(
            cliente=self.cliente,
            servizio=self.servizio,
            quantita=3,
            data_servizio=datetime.datetime(2026, 7, 1, 10, 0),
            indirizzo_intervento="indirizzo",
        )
        self.assertEqual(p.totale, Decimal("30.00"))

    def test_esegue_assignment_unique(self):
        Esegue.objects.create(staff=self.staff, servizio=self.servizio)
        # creare un duplicato deve dare IntegrityError per via di unique_together
        with self.assertRaises(IntegrityError):
            Esegue.objects.create(staff=self.staff, servizio=self.servizio)
