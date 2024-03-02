#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fin23.settings")

import django

django.setup()

def main():

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fin23.settings')
    #settings.configure()
    #os.environ['DJANGO_SETTINGS_MODULE'] = 'fin23.settings'

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("error") from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
