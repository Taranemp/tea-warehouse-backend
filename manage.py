#!/usr/bin/env python
import os
import sys

def main():
    if "DJANGO_SETTINGS_MODULE" not in os.environ:
        # Set env to dev for local development
        os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.dev"

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed."
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()