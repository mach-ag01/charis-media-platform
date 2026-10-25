FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "echo '=== BOOKINGS MIGRATION FILES ===' && ls -la bookings/migrations && echo '=== BOOKINGS APP CONFIG ===' && python manage.py shell -c \"from django.apps import apps; c=apps.get_app_config('bookings'); print('App path:', c.path); print('Models:', [m.__name__ for m in c.get_models()])\" && echo '=== BOOKINGS MIGRATION STATUS ===' && python manage.py showmigrations bookings && echo '=== MIGRATION PLAN ===' && python manage.py migrate --plan && echo '=== APPLY MIGRATIONS ===' && python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
