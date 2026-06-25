# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Gabriele
import json

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ClienteRegistrationForm,
    PrenotazioneForm,
    ServizioPuliziaForm,
    StatoPrenotazioneForm,
)
from .models import Cliente, Esegue, Prenotazione, ProfiloUtente, ServizioPulizia, Staff


def is_admin_user(user):
    return user.is_superuser or getattr(getattr(user, "profiloutente", None), "ruolo", None) == ProfiloUtente.RUOLO_ADMIN


def is_staff_user(user):
    return user.is_staff or getattr(getattr(user, "profiloutente", None), "ruolo", None) in [
        ProfiloUtente.RUOLO_STAFF,
        ProfiloUtente.RUOLO_ADMIN,
    ]


def get_cliente_for_user(user):
    return Cliente.objects.filter(user=user).first()


def can_create_prenotazione(user):
    return user.is_authenticated and get_cliente_for_user(user) is not None


def home(request):
    servizi = ServizioPulizia.objects.all()[:6]
    return render(
        request,
        "gestionale/home.html",
        {"servizi": servizi, "can_create_prenotazione": can_create_prenotazione(request.user)},
    )


def register(request):
    if request.method == "POST":
        form = ClienteRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registrazione completata.")
            return redirect("dashboard_cliente")
    else:
        form = ClienteRegistrationForm()
    return render(request, "gestionale/register.html", {"form": form})


@login_required
def dashboard(request):
    if is_admin_user(request.user):
        return redirect("dashboard_admin")
    if is_staff_user(request.user):
        return redirect("dashboard_staff")
    return redirect("dashboard_cliente")


@login_required
def dashboard_cliente(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    prenotazioni = cliente.prenotazioni.all()[:5]
    return render(request, "gestionale/dashboard_cliente.html", {"cliente": cliente, "prenotazioni": prenotazioni})


@login_required
@user_passes_test(is_staff_user)
def dashboard_staff(request):
    staff = Staff.objects.filter(user=request.user).first()
    servizi_eseguiti = (
        Esegue.objects.select_related("servizio").filter(staff=staff)
        if staff
        else []
    )
    return render(
        request,
        "gestionale/dashboard_staff.html",
        {"staff": staff, "servizi_eseguiti": servizi_eseguiti},
    )


@login_required
@user_passes_test(is_admin_user)
def dashboard_admin(request):
    context = {
        "prenotazioni_count": Prenotazione.objects.count(),
        "clienti_count": Cliente.objects.count(),
        "servizi_count": ServizioPulizia.objects.count(),
        "staff_count": Staff.objects.count(),
        "prenotazioni_recenti": Prenotazione.objects.select_related("cliente")[:8],
    }
    return render(request, "gestionale/dashboard_admin.html", context)


@login_required
def lista_prenotazioni(request):
    if is_admin_user(request.user) or is_staff_user(request.user):
        prenotazioni = Prenotazione.objects.select_related("cliente", "servizio").all()
    else:
        cliente = get_object_or_404(Cliente, user=request.user)
        prenotazioni = cliente.prenotazioni.select_related("servizio").all()
    return render(
        request,
        "gestionale/lista_prenotazioni.html",
        {"prenotazioni": prenotazioni, "can_create_prenotazione": can_create_prenotazione(request.user)},
    )


@login_required
def dettaglio_prenotazione(request, pk):
    prenotazione = get_object_or_404(Prenotazione.objects.select_related("cliente", "servizio"), pk=pk)
    if not (is_admin_user(request.user) or is_staff_user(request.user) or prenotazione.cliente.user == request.user):
        messages.error(request, "Non hai i permessi per visualizzare questa prenotazione.")
        return redirect("lista_prenotazioni")

    stato_form = StatoPrenotazioneForm(instance=prenotazione)
    can_manage_status = is_staff_user(request.user)
    return render(
        request,
        "gestionale/dettaglio_prenotazione.html",
        {
            "prenotazione": prenotazione,
            "stato_form": stato_form,
            "can_manage_status": can_manage_status,
        },
    )


@login_required
def crea_prenotazione(request):
    cliente = get_cliente_for_user(request.user)
    if cliente is None:
        messages.error(request, "Solo gli utenti cliente possono creare una nuova prenotazione.")
        return redirect("lista_prenotazioni")

    if request.method == "POST":
        form = PrenotazioneForm(request.POST)
        if form.is_valid():
            prenotazione = form.save(commit=False)
            prenotazione.cliente = cliente
            prenotazione.save()
            messages.success(request, "Prenotazione creata.")
            return redirect("dettaglio_prenotazione", pk=prenotazione.pk)
    else:
        form = PrenotazioneForm()
    prezzi = {str(s.pk): float(s.prezzo_base) for s in ServizioPulizia.objects.all()}
    return render(request, "gestionale/form_prenotazione.html", {"form": form, "prezzi_json": json.dumps(prezzi)})


@login_required
@user_passes_test(is_staff_user)
def modifica_stato_prenotazione(request, pk):
    prenotazione = get_object_or_404(Prenotazione, pk=pk)
    if request.method == "POST":
        form = StatoPrenotazioneForm(request.POST, instance=prenotazione)
        if form.is_valid():
            form.save()
            messages.success(request, "Stato aggiornato.")
    return redirect("dettaglio_prenotazione", pk=pk)


@login_required
@user_passes_test(is_admin_user)
def servizio_list(request):
    servizi = ServizioPulizia.objects.all()
    return render(request, "gestionale/lista_servizi.html", {"servizi": servizi})


@login_required
@user_passes_test(is_admin_user)
def servizio_create(request):
    if request.method == "POST":
        form = ServizioPuliziaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Servizio creato.")
            return redirect("servizio_list")
    else:
        form = ServizioPuliziaForm()
    return render(request, "gestionale/form_servizio.html", {"form": form, "titolo": "Nuovo servizio"})


@login_required
@user_passes_test(is_admin_user)
def servizio_update(request, pk):
    servizio = get_object_or_404(ServizioPulizia, pk=pk)
    if request.method == "POST":
        form = ServizioPuliziaForm(request.POST, instance=servizio)
        if form.is_valid():
            form.save()
            messages.success(request, "Servizio aggiornato.")
            return redirect("servizio_list")
    else:
        form = ServizioPuliziaForm(instance=servizio)
    return render(request, "gestionale/form_servizio.html", {"form": form, "titolo": "Modifica servizio"})


@login_required
@user_passes_test(is_admin_user)
def servizio_delete(request, pk):
    servizio = get_object_or_404(ServizioPulizia, pk=pk)
    if request.method == "POST":
        servizio.delete()
        messages.success(request, "Servizio eliminato.")
        return redirect("servizio_list")
    return render(request, "gestionale/conferma_eliminazione_servizio.html", {"servizio": servizio})
