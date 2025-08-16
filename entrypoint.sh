#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] Aplicando migrações..."
python manage.py migrate --noinput

echo "[entrypoint] Coletando estáticos..."
python manage.py collectstatic --noinput

# Criação automática do superuser, se variáveis de ambiente estiverem definidas
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    echo "[entrypoint] Criando superuser (se não existir)..."
    python manage.py shell <<END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
END
fi

echo "[entrypoint] Iniciando Gunicorn..."
exec gunicorn ecotrip_admin.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers ${GUNICORN_WORKERS:-3} \
  --threads ${GUNICORN_THREADS:-2} \
  --timeout ${GUNICORN_TIMEOUT:-60} \
  --access-logfile - \
  --error-logfile -
