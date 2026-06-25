from django.apps import AppConfig


class GestionaleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gestionale"

    def ready(self):
        # Import signal handlers to register them when the app is ready
        try:
            import gestionale.signals  # noqa: F401
        except Exception:
            # Avoid crashing import if signals file has issues; errors will surface during runtime
            pass
