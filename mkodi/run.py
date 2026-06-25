#!/usr/bin/env python
import os
import ssl
import sys
from pathlib import Path

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.utils.autoreload import run_with_reloader

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mkodi.settings")
import django
django.setup()

BASE_DIR = Path(__file__).resolve().parent
CERT_FILE = BASE_DIR / "devserver.crt"
KEY_FILE = BASE_DIR / "devserver.key"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 3000


def parse_bind_arg(argv):
    host = DEFAULT_HOST
    port = DEFAULT_PORT
    for arg in argv:
        if arg.startswith("-"):
            continue
        if arg == "runserver":
            continue
        if arg in ("--help", "-h", "--version"):
            return None, None
        if ":" in arg:
            host_part, port_part = arg.rsplit(":", 1)
            host = host_part or DEFAULT_HOST
            try:
                port = int(port_part)
            except ValueError:
                return None, None
            return host, port
        try:
            port = int(arg)
            return host, port
        except ValueError:
            host = arg
    return host, port


def generate_dev_cert(cert_path: Path, key_path: Path) -> None:
    if cert_path.exists() and key_path.exists():
        return

    try:
        from cryptography import x509
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.x509.oid import NameOID
        from datetime import datetime, timedelta
    except ImportError as exc:
        raise RuntimeError(
            "cryptography is required to generate a local development HTTPS certificate. "
            "Install it in your environment and rerun the server."
        ) from exc

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])
    now = datetime.utcnow()
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(days=1))
        .not_valid_after(now + timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("127.0.0.1"),
            ]),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )

    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    print(f"Created local HTTPS certificate: {cert_path} and {key_path}")


def run_server(host=DEFAULT_HOST, port=DEFAULT_PORT, use_reloader=True) -> None:
    generate_dev_cert(CERT_FILE, KEY_FILE)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=str(CERT_FILE), keyfile=str(KEY_FILE))
    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2

    application = get_wsgi_application()
    if settings.DEBUG:
        try:
            from django.contrib.staticfiles.handlers import StaticFilesHandler
            application = StaticFilesHandler(application)
        except ImportError:
            pass

    from wsgiref.simple_server import make_server

    with make_server(host, port, application) as httpd:
        httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
        print(f"Starting HTTPS development server at https://{host}:{port}/")
        print("If your browser warns about an untrusted certificate, accept the warning for local development.")
        httpd.serve_forever()


if __name__ == "__main__":
    bind_host, bind_port = parse_bind_arg(sys.argv[1:])
    if bind_host is None:
        raise SystemExit("Invalid runserver arguments")
    if len(sys.argv) > 1 and "--noreload" in sys.argv:
        run_server(bind_host, bind_port, use_reloader=False)
    else:
        run_with_reloader(lambda: run_server(bind_host, bind_port))
