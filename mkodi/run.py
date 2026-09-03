#!/usr/bin/env python
import os
import subprocess
import sys


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 3000


def _build_runserver_args(argv):
    if len(argv) > 1:
        return ["manage.py", "runserver", *argv[1:]]
    return ["manage.py", "runserver", "3000"]


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mkodi.settings")
    args = _build_runserver_args(sys.argv)
    subprocess.run([sys.executable, *args], check=False)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    bind_host, bind_port = parse_bind_arg(sys.argv[1:])
    if bind_host is None:
        raise SystemExit("Invalid runserver arguments")
    if len(sys.argv) > 1 and "--noreload" in sys.argv:
        run_server(bind_host, bind_port, use_reloader=False)
    else:
        run_with_reloader(lambda: run_server(bind_host, bind_port))
