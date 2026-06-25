# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Gabriele
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class ProfiloUtente(models.Model):
    RUOLO_CLIENTE = "Cliente"
    RUOLO_STAFF = "Staff"
    RUOLO_ADMIN = "Admin"

    RUOLO_CHOICES = [
        (RUOLO_CLIENTE, "Cliente"),
        (RUOLO_STAFF, "Staff"),
        (RUOLO_ADMIN, "Admin"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=30)
    ruolo = models.CharField(max_length=20, choices=RUOLO_CHOICES, default=RUOLO_CLIENTE)

    class Meta:
        verbose_name = "Profilo utente"
        verbose_name_plural = "Profili utente"

    def __str__(self):
        return f"{self.user.username} - {self.ruolo}"


class Cliente(models.Model):
    TIPO_PRIVATO = "Privato"
    TIPO_AZIENDA = "Azienda"

    TIPO_CLIENTE_CHOICES = [
        (TIPO_PRIVATO, "Privato"),
        (TIPO_AZIENDA, "Azienda"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)
    email = models.EmailField()
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE_CHOICES)
    codice_fiscale = models.CharField(max_length=16, null=True, blank=True)
    indirizzo_abitazione = models.CharField(max_length=255, null=True, blank=True)
    partita_iva = models.CharField(max_length=20, null=True, blank=True)
    sede_legale = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"

    def __str__(self):
        return f"{self.nome} {self.cognome}"


class Staff(models.Model):
    RUOLO_TITOLARE = "Titolare"
    RUOLO_CAPO_AREA = "Capo area"
    RUOLO_CAPO_SQUADRA = "Capo squadra"
    RUOLO_OPERAIO = "Operaio"

    RUOLO_CHOICES = [
        (RUOLO_TITOLARE, "Titolare"),
        (RUOLO_CAPO_AREA, "Capo area"),
        (RUOLO_CAPO_SQUADRA, "Capo squadra"),
        (RUOLO_OPERAIO, "Operaio"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    ruolo = models.CharField(max_length=20, choices=RUOLO_CHOICES)
    specializzazione = models.CharField(max_length=150, null=True, blank=True)
    quota_societaria = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    area_competenza = models.CharField(max_length=100, null=True, blank=True)
    numero_squadra = models.CharField(max_length=50, null=True, blank=True)
    disponibilita = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.nome} {self.cognome} - {self.ruolo}"


class ServizioPulizia(models.Model):
    TIPO_ORDINARIA = "Ordinaria"
    TIPO_STRAORDINARIA = "Straordinaria"
    TIPO_SANIFICAZIONE = "Sanificazione"

    TIPO_SERVIZIO_CHOICES = [
        (TIPO_ORDINARIA, "Ordinaria"),
        (TIPO_STRAORDINARIA, "Straordinaria"),
        (TIPO_SANIFICAZIONE, "Sanificazione"),
    ]

    nome = models.CharField(max_length=120)
    descrizione = models.TextField()
    prezzo_base = models.DecimalField(max_digits=10, decimal_places=2)
    durata_stimata = models.DurationField(help_text="Formato consigliato: HH:MM:SS")
    tipo_servizio = models.CharField(max_length=30, choices=TIPO_SERVIZIO_CHOICES)
    frequenza = models.CharField(max_length=100, null=True, blank=True)
    livello_sporco = models.CharField(max_length=100, null=True, blank=True)
    prodotto_utilizzato = models.CharField(max_length=150, null=True, blank=True)
    certificazione_richiesta = models.BooleanField(default=False)
    recensione = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Servizio di pulizia"
        verbose_name_plural = "Servizi di pulizia"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.tipo_servizio})"

    def get_absolute_url(self):
        return reverse("servizio_update", kwargs={"pk": self.pk})


class Prenotazione(models.Model):
    STATO_IN_ATTESA = "In attesa"
    STATO_CONFERMATA = "Confermata"
    STATO_COMPLETATA = "Completata"
    STATO_ANNULLATA = "Annullata"

    STATO_CHOICES = [
        (STATO_IN_ATTESA, "In attesa"),
        (STATO_CONFERMATA, "Confermata"),
        (STATO_COMPLETATA, "Completata"),
        (STATO_ANNULLATA, "Annullata"),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="prenotazioni")
    servizio = models.ForeignKey(ServizioPulizia, on_delete=models.PROTECT, related_name="prenotazioni")
    quantita = models.PositiveIntegerField(default=1)
    data_richiesta = models.DateTimeField(auto_now_add=True)
    data_servizio = models.DateTimeField()
    stato = models.CharField(max_length=20, choices=STATO_CHOICES, default=STATO_IN_ATTESA)
    indirizzo_intervento = models.CharField(max_length=255)
    importo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    metodo_pagamento = models.CharField(max_length=100, null=True, blank=True)
    data_pagamento = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Prenotazione"
        verbose_name_plural = "Prenotazioni"
        ordering = ["-data_servizio"]

    def __str__(self):
        return f"Prenotazione #{self.pk} - {self.cliente}"

    @property
    def totale(self):
        return self.servizio.prezzo_base * self.quantita


class Esegue(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="servizi_eseguiti")
    servizio = models.ForeignKey(ServizioPulizia, on_delete=models.CASCADE, related_name="staff_esecutori")

    class Meta:
        verbose_name = "Esecuzione"
        verbose_name_plural = "Esecuzioni"
        unique_together = ("staff", "servizio")

    def __str__(self):
        return f"{self.staff} → {self.servizio}"


class Squadra(models.Model):
    nome_squadra = models.CharField(max_length=100)
    zona_operativa = models.CharField(max_length=150)
    composta_da = models.ManyToManyField(Staff, related_name="squadre")

    class Meta:
        verbose_name = "Squadra"
        verbose_name_plural = "Squadre"

    def __str__(self):
        return f"{self.nome_squadra} ({self.zona_operativa})"


class Prodotto(models.Model):
    nome_prodotto = models.CharField(max_length=120)
    tipo_prodotto = models.CharField(max_length=100)
    utilizza = models.ManyToManyField(ServizioPulizia, related_name="prodotti")

    class Meta:
        verbose_name = "Prodotto"
        verbose_name_plural = "Prodotti"

    def __str__(self):
        return f"{self.nome_prodotto} ({self.tipo_prodotto})"
