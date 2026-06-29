from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Esegue, Prenotazione


# Trigger 1: calcola l'importo prima di salvare la prenotazione
@receiver(pre_save, sender=Prenotazione)
def calcola_importo(sender, instance, **kwargs):
    """Calcola importo = prezzo_base * quantita ogni volta che si salva una prenotazione."""
    if instance.servizio_id:
        instance.importo = instance.servizio.prezzo_base * instance.quantita


# Trigger 2a: quando uno staff viene assegnato a un servizio, diventa non disponibile
@receiver(post_save, sender=Esegue)
def segna_staff_non_disponibile(sender, instance, created, **kwargs):
    """Alla creazione di un'assegnazione, lo staff viene messo come non disponibile."""
    if created:
        instance.staff.disponibilita = False
        instance.staff.save(update_fields=["disponibilita"])


# Trigger 2b: quando l'assegnazione viene rimossa, lo staff torna disponibile
@receiver(post_delete, sender=Esegue)
def segna_staff_disponibile(sender, instance, **kwargs):
    """Se lo staff non ha più assegnazioni attive, torna disponibile."""
    ha_altre_assegnazioni = Esegue.objects.filter(staff=instance.staff).exists()
    if not ha_altre_assegnazioni:
        instance.staff.disponibilita = True
        instance.staff.save(update_fields=["disponibilita"])


# Trigger 3: quando una prenotazione viene completata, registra la data di pagamento
@receiver(post_save, sender=Prenotazione)
def registra_data_pagamento(sender, instance, **kwargs):
    """Se la prenotazione è Completata e ha un metodo di pagamento, salva la data."""
    if (
        instance.stato == Prenotazione.STATO_COMPLETATA
        and instance.metodo_pagamento
        and not instance.data_pagamento
    ):
        Prenotazione.objects.filter(pk=instance.pk).update(data_pagamento=timezone.now())
