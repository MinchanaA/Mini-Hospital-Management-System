# Mini-Hospital-Management-System


A state-of-the-art, high-performance Hospital Management System featuring a high-end **Glassmorphism UI**, **Asynchronous Email Notifications**, and **Seamless Google Calendar Integration**.

---

## Overview

Mini HMS is a modern web application designed to bridge the gap between healthcare providers and patients. Unlike traditional hospital systems, Mini HMS focuses on **User Experience (UX)** and **Performance**, utilizing an asynchronous architecture to handle secondary tasks like notifications and calendar synchronization without blocking the main user flow.

## System Architecture

The project is split into two primary services:

1.  **Django Backend (Monolith)**:
    *   Handles authentication, scheduling logic, and doctor/patient data management.
    *   Exposes a responsive web interface built with Django Templates.
    *   Uses **PostgreSQL** for robust data persistence.
2.  **Email Notification Service (Microservice)**:
    *   Built with **Node.js** and **Serverless Offline**.
    *   Runs on port `3000`.
    *   Handles all outbound SMTP communication asynchronously via Gmail.

---

## Key Features

### Dual-Role Portals
*   **Doctor Portal**: Doctors can create availability slots, manage their specialized profile (specialization, bio), and view their upcoming appointments.
*   **Patient Portal**: Patients can browse specialized doctors, view available time slots in real-time, and book appointments with a single click.

### Smart Scheduling
*   **Real-time Availability**: Slots are color-coded based on status (Available/Booked).
*   **Conflict Prevention**: One-to-one mapping between appointments and availability slots ensures no double-booking.

### Asynchronous Notifications
*   **Welcome Emails**: Sent automatically upon registration using Django Signals (`post_save`).
*   **Booking Confirmations**: Immediate confirmation sent to patients after a successful booking.
*   **Non-blocking**: All emails are sent via a separate thread to ensure a snappy UI.

### Google Calendar Integration
*   **Automated Sync**: Every booking creates a corresponding event in the doctor's Google Calendar.
*   **Silent Authentication**: Uses pre-configured OAuth tokens to ensure patients aren't interrupted by Google login redirects during the booking process.

---

## Design System: Glassmorphism Royale

The UI follows a strict **Glassmorphism** design language, characterized by:
*   **Translucency**: Frosted glass cards with background blur (`backdrop-filter`).
*   **Vibrant Gradients**: A curated palette of Deep Indigo (`#4f46e5`), Electric Blue (`#0ea5e9`), and Rose Pink (`#f472b6`).
*   **Micro-animations**: Smooth hover transitions, staggered grid entrances, and loading states.
*   **Typography**: Using the 'Outfit' Google Font for a clean, modern aesthetic.

---

## Data Models

### Users App
*   **User**: Extended Django User model with `is_doctor` and `is_patient` flags.
*   **DoctorProfile**: Stores specialization and detailed bio.
*   **PatientProfile**: Stores date of birth and contact information.

### Appointments App
*   **Availability**: Represents a time block created by a doctor.
*   **Appointment**: Links a patient to a specific availability slot.

---

## Technical Implementation Details

### Asynchronous Flow
When a user registers or books an appointment, the Django backend triggers a thread:
1.  Django prepares the email payload (type, recipient, data).
2.  A separate Python thread sends an HTTP POST request to the Serverless service on port 3000.
3.  The Serverless service uses `smtplib` to dispatch the email.
4.  The user's request finishes instantly, even if the email takes 2-3 seconds to send.

### Google Calendar Logic
*   Located in `appointments/calendar_utils.py`.
*   Uses `google-api-python-client` and `google-auth-oauthlib`.
*   Handles token refresh automatically.
*   Gracefully falls back (logs error) if the calendar service is unavailable, ensuring the appointment is still saved in the local database.

---

## Detailed Setup Instructions

### 1. Prerequisites
*   Python 3.10+
*   Node.js (for Email Service)
*   PostgreSQL Database

### 2. Backend Setup
```bash
cd hms_backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

### 3. Email Service Setup
```bash
cd email_service
npm install
```

### 4. Running the Project
Use the provided `run.sh` at the root directory:
```bash
./run.sh
```
This script uses `lsof` to clear any ports (8000/3000) and starts both services in parallel.

---

## 📂 Project Structure

```text
├── hms_backend/           # Django Project Root
│   ├── appointments/      # Appointment & Calendar logic
│   ├── users/            # User models & Email utils
│   ├── templates/         # Glassmorphism HTML templates
│   ├── static/           # Global CSS and JS
│   └── manage.py
├── email_service/         # Serverless Email Worker
│   ├── handler.py         # SMTP logic
│   └── serverless.yml
└── run.sh                 # Global Startup Script
```

---

*This project was developed as a high-end HMS demonstration, focusing on modern web standards and architectural excellence.*
