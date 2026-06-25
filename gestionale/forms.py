# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Gabriele
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Cliente, Prenotazione, ProfiloUtente, ServizioPulizia


class ClienteRegistrationForm(UserCreationForm):
    nome = forms.CharField(max_length=100)
    cognome = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=30)
    email = forms.EmailField()
    tipo_cliente = forms.ChoiceField(choices=Cliente.TIPO_CLIENTE_CHOICES)
    codice_fiscale = forms.CharField(max_length=16, required=False)
    indirizzo_abitazione = forms.CharField(max_length=255, required=False)
    partita_iva = forms.CharField(max_length=20, required=False)
    sede_legale = forms.CharField(max_length=255, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["nome"]
        user.last_name = self.cleaned_data["cognome"]
        if commit:
            user.save()
            Cliente.objects.create(
                user=user,
                nome=self.cleaned_data["nome"],
                cognome=self.cleaned_data["cognome"],
                telefono=self.cleaned_data["telefono"],
                email=self.cleaned_data["email"],
                tipo_cliente=self.cleaned_data["tipo_cliente"],
                codice_fiscale=self.cleaned_data["codice_fiscale"],
                indirizzo_abitazione=self.cleaned_data["indirizzo_abitazione"],
                partita_iva=self.cleaned_data["partita_iva"],
                sede_legale=self.cleaned_data["sede_legale"],
            )
            ProfiloUtente.objects.create(user=user, telefono=self.cleaned_data["telefono"], ruolo=ProfiloUtente.RUOLO_CLIENTE)
        return user


class ServizioPuliziaForm(forms.ModelForm):
    class Meta:
        model = ServizioPulizia
        fields = [
            "nome",
            "descrizione",
            "prezzo_base",
            "durata_stimata",
            "tipo_servizio",
            "frequenza",
            "livello_sporco",
            "prodotto_utilizzato",
            "certificazione_richiesta",
            "recensione",
        ]
        widgets = {
            "descrizione": forms.Textarea(attrs={"rows": 4}),
            "durata_stimata": forms.TextInput(attrs={"placeholder": "HH:MM:SS"}),
        }


class ServizioPuliziaChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome} (€{obj.prezzo_base})"


class PrenotazioneForm(forms.ModelForm):
    servizio = ServizioPuliziaChoiceField(queryset=ServizioPulizia.objects.all())

    class Meta:
        model = Prenotazione
        fields = ["servizio", "quantita", "data_servizio", "indirizzo_intervento"]
        widgets = {
            "data_servizio": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class StatoPrenotazioneForm(forms.ModelForm):
    class Meta:
        model = Prenotazione
        fields = ["stato"]
