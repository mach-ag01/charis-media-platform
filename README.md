# Charis Digital Crafts Media House — Booking & Production Platform

A responsive, mobile-friendly web app starter for the Charis Digital Crafts Media House intake questionnaire. It includes a client-facing website, multi-step booking intake, admin dashboard, booking management, production board, client directory, payment milestone tracking and Django REST API.

## Included

- Client website with service catalogue and booking call-to-action
- Multi-step intake form based on the provided questionnaire
- Services: videography, photography, branding/identity, digital marketing/UI
- Package choices: Silver, Gold, Platinum, custom/hourly, studio, outdoor, half-day, full-day, corporate identity, stationery, typography/slogan, web mockups, social retainer and Reels
- Event date, venue, coverage area and project brief
- Required acknowledgements for recording/privacy, production coordination and 70%/30% financial milestones
- Admin dashboard with overview metrics
- Booking list, status filters, CSV export and booking details drawer
- Production board with status updates, crew assignment and delivery link
- Client directory and payment milestone register
- Django REST Framework API, Django admin and PostgreSQL
- Docker Compose setup; Node.js runs inside a container, not on the host

## Run on Windows with Docker Desktop

1. Install and start Docker Desktop.
2. Extract this project folder.
3. Open PowerShell in the extracted `charis-media-platform` folder.
4. Run:

   ```powershell
   docker compose up --build
   ```

5. Open:
   - Web app: http://localhost:5173
   - API health: http://localhost:8000/
   - Booking API: http://localhost:8000/api/bookings/
   - Dashboard API: http://localhost:8000/api/dashboard/
   - Django admin: http://localhost:8000/admin/

Stop with `Ctrl+C`, or run `docker compose down`. Database data is kept in the Docker volume. To reset local development data, run `docker compose down -v`.

## First-time admin account

In a second PowerShell window:

```powershell
docker compose exec backend python manage.py createsuperuser
```

Use that account at `/admin/`. The admin site is useful for reviewing all bookings and production tasks.

## Typical workflow

1. Client opens the website and chooses **Start a project**.
2. Client supplies contact details and selects services/packages.
3. Client provides event date, venue, coverage and brief.
4. Client checks all three acknowledgements and submits the enquiry.
5. Admin reviews the enquiry in Bookings, sets the quotation and status.
6. Admin assigns crew, tracks production and adds a delivery link.
7. Admin records deposit and balance payments in Payments.

The default milestone calculation is 70% deposit and 30% balance. The quote starts at KES 0 because actual prices must be set by the business; no rates are invented.

## API endpoints

- `GET/POST /api/bookings/`
- `GET/PATCH/PUT/DELETE /api/bookings/<id>/`
- `GET/POST /api/tasks/`
- `GET /api/dashboard/`

## Important limitations before public launch

This is a functional **starter MVP**, not yet a production-secure service.

- API endpoints are open for local demonstration. Before launch, implement authentication, role-based permissions, customer ownership checks, validation, throttling and audit logging.
- M-Pesa is not integrated. Add Daraja STK Push, secure callback verification, idempotency, reconciliation and a sandbox test plan before live collections.
- Email/SMS/WhatsApp notifications are not wired up.
- File delivery is currently a URL field; add private object storage, access controls and expiring download links for confidential media.
- Add tests, monitoring, backups, privacy notice, retention rules and a deployment secret manager.
- The questionnaire's legal acknowledgements are represented as operational intake checkboxes; have a qualified Kenyan legal/privacy professional review the final wording and workflow.
- Change `SECRET_KEY`, disable `DEBUG`, restrict `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`, use HTTPS, and configure production database credentials before deployment.

## Technology

- Frontend: React + Vite + Lucide icons
- Backend: Django + Django REST Framework
- Database: PostgreSQL
- Local orchestration: Docker Compose

## Project structure

```text
charis-media-platform/
├── docker-compose.yml
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── config/
│   └── bookings/
└── frontend/
    ├── package.json
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx
        └── styles.css
```

## Quality and evaluation checklist

| Evaluation area | What this project provides | Suggested verification |
|---|---|---|
| Code quality & structure (25%) | Separate React frontend and Django app/config, serializers, viewsets, models, migrations and admin configuration | Review `frontend/src/` and `backend/bookings/`; run tests below |
| Functionality (35%) | Intake submissions, booking/status management, dashboard aggregates, production tasks and 70/30 payment calculations | Submit a test booking and update it through Django admin |
| UI/UX (20%) | Responsive client intake and management interface with service/package selection and clear booking states | Test at desktop and mobile viewport sizes |
| Documentation (10%) | Setup instructions, endpoints, workflow, structure and limitations documented here | Follow the clean-start instructions |
| Bonus (10%) | CSV export, status filtering, production tasks, payment milestone tracking and API tests | Run tests and try the dashboard workflow |

## Run automated backend tests

```powershell
docker compose exec backend python manage.py test bookings
```

## Clean start

```powershell
docker compose down
# Optional: this deletes local PostgreSQL data too
# docker compose down -v
docker compose up --build
```

## Before production deployment

This is a development MVP. The API is intentionally open for local evaluation and **must not be exposed to the public internet as-is**. Before production, implement authenticated customer/admin/crew roles and object-level permissions; add rate limiting and audit logs; move credentials into a secrets manager; configure HTTPS, secure cookies, backups and monitoring; and add privacy-reviewed consent copy. M-Pesa, email, SMS, WhatsApp and secure media storage are not integrated in this build. Do not represent them as working features until implemented and tested.
