#!/bin/sh
set -e

# Ensure storage directories exist
mkdir -p /app/storage/database \
         /app/storage/cache \
         /app/storage/cover \
         /app/storage/logs \
         /app/storage/avatars

# Run migrations
alembic upgrade head

# Initialize default settings
python - << 'EOF'
from app.database import SessionLocal
from app.services.settings_service import SettingsService

db = SessionLocal()
SettingsService(db).initialize_defaults()
db.close()
EOF

# Start Uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4