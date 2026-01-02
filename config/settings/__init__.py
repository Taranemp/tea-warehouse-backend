import os
import pymysql

pymysql.install_as_MySQLdb()

# Ensure DJANGO_SETTINGS_MODULE is defined
if "DJANGO_SETTINGS_MODULE" not in os.environ:
    raise RuntimeError(
        "DJANGO_SETTINGS_MODULE is not set. "
        "It must be defined by Passenger (prod) or manually (dev)."
    )
