#!/bin/bash
# Start Serverless Offline
echo "Starting Email Service (Serverless Offline)..."
cd email_service
npm install  # Ensure dependencies
nohup npx serverless offline --host 0.0.0.0 --port 3000 > ../email_service.log 2>&1 &
EMAIL_PID=$!
echo "Email Service started (PID: $EMAIL_PID)"

# Start Django Server
echo "Starting Django Server..."
cd ../hms_backend
source .venv/bin/activate
python manage.py migrate # Ensure latest migrations
python manage.py runserver 0.0.0.0:8000
