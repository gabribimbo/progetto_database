# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Gabriele
from django.contrib import admin

from .models import Cliente, Esegue, Prenotazione, ProfiloUtente, Prodotto, ServizioPulizia, Squadra, Staff


@admin.register(ProfiloUtente)
class ProfiloUtenteAdmin(admin.ModelAdmin):
    list_display = ("user", "telefono", "ruolo")
    list_filter = ("ruolo",)
    search_fields = ("user__username", "user__email", "telefono")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "cognome", "email", "telefono", "tipo_cliente")
    list_filter = ("tipo_cliente",)
    search_fields = ("nome", "cognome", "email", "codice_fiscale", "partita_iva")


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("nome", "cognome", "ruolo", "specializzazione", "disponibilita")
    list_filter = ("disponibilita", "ruolo")
    search_fields = ("nome", "cognome", "ruolo", "specializzazione")


class EsegueInline(admin.TabularInline):
    model = Esegue
    extra = 1


@admin.register(ServizioPulizia)
class ServizioPuliziaAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo_servizio", "prezzo_base", "durata_stimata", "certificazione_richiesta")
    list_filter = ("tipo_servizio", "certificazione_richiesta")
    search_fields = ("nome", "descrizione", "prodotto_utilizzato")
    inlines = [EsegueInline]


@admin.register(Prenotazione)
class PrenotazioneAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "servizio", "quantita", "data_richiesta", "data_servizio", "stato", "indirizzo_intervento")
    list_filter = ("stato", "data_servizio")
    search_fields = ("cliente__nome", "cliente__cognome", "servizio__nome", "indirizzo_intervento")
    date_hierarchy = "data_servizio"


@admin.register(Esegue)
class EsegueAdmin(admin.ModelAdmin):
    list_display = ("staff", "servizio")
    search_fields = ("staff__nome", "staff__cognome", "servizio__nome")


@admin.register(Squadra)
class SquadraAdmin(admin.ModelAdmin):
    list_display = ("nome_squadra", "zona_operativa")
    search_fields = ("nome_squadra", "zona_operativa")
    filter_horizontal = ("composta_da",)


@admin.register(Prodotto)
class ProdottoAdmin(admin.ModelAdmin):
    list_display = ("nome_prodotto", "tipo_prodotto")
    list_filter = ("tipo_prodotto",)
    search_fields = ("nome_prodotto", "tipo_prodotto")
    filter_horizontal = ("utilizza",)
