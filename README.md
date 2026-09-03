# MKodi

MKodi is a Django portal for taxpayer profiles, revenue intelligence, and payment activity.

## Local setup

From the `mkodi` directory:

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 3000
```

Open the portal at `http://127.0.0.1:3000/` and admin at `http://127.0.0.1:3000/admin/`.

## Demo flow

1. Create a taxpayer record in Django admin with the TIN, NIDA, business, BRELA, land, income, and score fields.
2. Register from `/signup/` using that TIN and a password.
3. Review the dashboard, 360-degree intelligence page, payment history, and profile page.
4. Create a payment request and verify it appears in the payment history.
5. Upload a profile image and change the account password from the Profile page.

## Admin tools

The admin area is the source of truth for taxpayer details. Taxpayer records can be searched, filtered, deleted, and exported as CSV. Payment records are also searchable and filterable by method and status.

## Tests

```powershell
python manage.py check
python manage.py test
```

The current payment and integration endpoints are demo flows. Connect them to TRA, GePG, BRELA, NIDA, and mobile-money credentials before production use.

## Production checklist

- Set a strong `SECRET_KEY` and `DEBUG=False` in environment variables.
- Configure `ALLOWED_HOSTS`, HTTPS, secure cookies, and a production WSGI/ASGI server.
- Replace demo payment and integration handlers with authenticated provider clients.
- Move SQLite to PostgreSQL and schedule encrypted backups.
- Django admin changes are recorded in the built-in admin LogEntry audit history.
- Create role groups such as `TRA Officer`, `Payment Officer`, and `Read-only Auditor` with only the permissions each role needs.
