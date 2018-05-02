#!/usr/bin/env python
import os
import sys

import dotenv

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_file = os.path.join(base_dir, '.env')
    if os.path.isfile(dotenv_file):
        dotenv.read_dotenv(base_dir)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
