from django.apps import AppConfig


class GestionaleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gestionale"

    def ready(self):
        # importa i signal per registrarli all'avvio dell'app
        try:
            import gestionale.signals  # noqa: F401
        except Exception:
            # evita il crash se il file signals ha problemi; gli errori emergono a runtime
            pass
