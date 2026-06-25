#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mkodi.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if len(sys.argv) >= 2 and sys.argv[1] == 'runserver':
        if any(arg in ('--help', '-h', '--version') for arg in sys.argv[1:]):
            execute_from_command_line(sys.argv)
            return
        try:
            from run import parse_bind_arg, run_server
        except ImportError:
            execute_from_command_line(sys.argv)
            return

        host, port = parse_bind_arg(sys.argv[1:])
        if host is not None:
            if '--noreload' in sys.argv:
                run_server(host, port, use_reloader=False)
            else:
                run_server(host, port)
            return

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
