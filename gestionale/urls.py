from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("registrazione/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/cliente/", views.dashboard_cliente, name="dashboard_cliente"),
    path("dashboard/staff/", views.dashboard_staff, name="dashboard_staff"),
    path("dashboard/admin/", views.dashboard_admin, name="dashboard_admin"),
    path("prenotazioni/", views.lista_prenotazioni, name="lista_prenotazioni"),
    path("prenotazioni/nuova/", views.crea_prenotazione, name="crea_prenotazione"),
    path("prenotazioni/<int:pk>/", views.dettaglio_prenotazione, name="dettaglio_prenotazione"),
    path("prenotazioni/<int:pk>/stato/", views.modifica_stato_prenotazione, name="modifica_stato_prenotazione"),
    path("servizi/", views.servizio_list, name="servizio_list"),
    path("servizi/nuovo/", views.servizio_create, name="servizio_create"),
    path("servizi/<int:pk>/modifica/", views.servizio_update, name="servizio_update"),
    path("servizi/<int:pk>/elimina/", views.servizio_delete, name="servizio_delete"),
]
