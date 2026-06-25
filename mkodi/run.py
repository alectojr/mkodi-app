#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mkodi.settings")
    django.setup()

    sys.argv = ['manage.py', 'runserver', '127.0.0.1:3000']
    execute_from_command_line(sys.argv)
