import os
from django.core.asgi import get_asgi_application

# DO NOT set a fallback here. Passenger or manage.py must set the correct DJANGO_SETTINGS_MODULE.
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    raise RuntimeError(
        "DJANGO_SETTINGS_MODULE is not set. "
        "Passenger or manage.py must set it before ASGI is loaded."
    )

application = get_asgi_application()
