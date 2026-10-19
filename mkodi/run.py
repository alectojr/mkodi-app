#!/usr/bin/env python
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 3000


def _build_runserver_args(argv):
    if len(argv) > 1:
        return ["manage.py", "runserver", *argv[1:]]
    return ["manage.py", "runserver", "3000"]


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mkodi.settings")
    manage_py = Path(__file__).resolve().with_name("manage.py")
    args = _build_runserver_args(sys.argv)
    args[0] = str(manage_py)
    subprocess.run([sys.executable, *args], cwd=manage_py.parent, check=True)


if __name__ == "__main__":
    main()
