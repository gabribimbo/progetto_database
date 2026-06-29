# Progetto Database - Servizio Pulizie

## Come avviare il progetto

```bash
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py runserver
```

Aprire il browser su:

```
http://localhost:8000
```

Il comando popola_db carica dei dati di esempio così si può provare l'app
senza doverla riempire a mano.

## Utenti di prova

La password per tutti è Password123!


admin_demo - amministratore, 
cliente_demo - cliente, 
staff_demo - staff.

## Struttura

La parte principale è nella cartella gestionale:


models.py - le tabelle del database (le entità).
signals.py - i trigger (calcolo importo, disponibilità staff, data pagamento).
views.py - le pagine e i permessi dei vari ruoli.
forms.py - i form.
i template HTML sono nella cartella templates.


## Licenza del progetto


Questo progetto è rilasciato sotto licenza MIT, il cui testo integrale e ufficiale si trova nel file LICENSE.
La licenza MIT è una delle licenze open source più diffuse ed è di tipo permissivo: stabilisce in modo esplicito a quali condizioni il codice può essere usato da altri. In sintesi consente a chiunque di usare, copiare, modificare e ridistribuire il software liberamente, anche per scopi commerciali, a una sola condizione: mantenere l'avviso di copyright e il testo della licenza nelle copie o nelle parti riutilizzate. La licenza include inoltre una clausola di esclusione di responsabilità: il software è fornito "così com'è", senza garanzie, e l'autore non risponde di eventuali danni derivanti dal suo utilizzo.
Serve a chiarire la titolarità del lavoro (l'autore resta riconosciuto come tale) e i termini con cui altri possono riutilizzarlo, evitando ambiguità: senza una licenza esplicita, infatti, per default tutti i diritti restano riservati e nessuno saprebbe se e come può legittimamente usare il codice.
