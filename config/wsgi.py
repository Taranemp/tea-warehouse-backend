import os
from django.core.wsgi import get_wsgi_application

# DO NOT set a fallback here. Passenger will set the correct DJANGO_SETTINGS_MODULE.
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    raise RuntimeError(
        "DJANGO_SETTINGS_MODULE is not set. "
        "Passenger or manage.py must set it before WSGI is loaded."
    )

application = get_wsgi_application()
