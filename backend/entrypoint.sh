#!/bin/bash
set -e

echo "================================================"
echo "🚀 Starting Passd Backend Application"
echo "================================================"

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
    echo "⏳ PostgreSQL is unavailable - sleeping"
    sleep 1
done
echo "✅ PostgreSQL is ready!"

# Apply database migrations
echo "📦 Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if DJANGO_SUPERUSER_USERNAME is set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Creating superuser..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='$DJANGO_SUPERUSER_EMAIL').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD', '$DJANGO_SUPERUSER_SALT')
    print('✅ Superuser created successfully!')
else:
    print('ℹ️  Superuser already exists.')
END
fi

echo "================================================"
echo "✅ Initialization complete!"
echo "🌐 Starting application server..."
echo "================================================"

# Execute the main command
exec "$@"
