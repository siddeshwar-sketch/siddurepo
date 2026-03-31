# All-in-One Donation Platform Implementation Plan

This document outlines the architecture and step-by-step implementation for the All-in-One Donation Platform built with Django. This platform is designed to be production-ready and scalable, catering to campaigns, donations, user management, and an administration dashboard.

## User Review Required

> [!WARNING]
> Please review the technology choices and open questions below before we begin the implementation. This is a very large undertaking, and establishing a robust foundation is critical.

## Proposed Architecture and Stack

**Backend**
*   **Framework:** Django 5.x & Django REST Framework (DRF)
*   **Database:** PostgreSQL (with SQLite for local fallback during initial setup if preferred)
*   **Caching & Task Queue:** Redis & Celery (for async tasks like email and payment verification)
*   **Authentication:** JWT (Simple JWT) + Session Auth (for Templates), AllAuth (for Social/Email)

**Frontend**
*   **UI:** Django Templates with Bootstrap 5 for the web interface, configured with a mobile-first responsive design strategy.
*   **JavaScript:** Vanilla JS + optional Alpine.js/jQuery for dynamic features without the overhead of an SPA, keeping it monolithic yet dynamic.
*   **API:** Fully functional DRF REST API for future React/Mobile integration.

**DevOps & Infrastructure**
*   **Containerization:** Docker & Docker Compose
*   **Web Server:** Gunicorn & Nginx
*   **Configuration:** `django-environ` for environment variable management.

## Proposed Changes

---

### Phase 1: Foundation and Configuration

Setup the base Django project and required application structures.

#### [NEW] `backend/config/` (Django Project Root)
*   `settings/base.py`, `settings/local.py`, `settings/production.py`
*   `urls.py`, `wsgi.py`, `asgi.py`
*   `.env.example`

#### [NEW] `backend/core/` (Core App)
*   Base models, utility functions, custom exceptions, mixins.

#### [NEW] `docker-compose.yml` & `Dockerfile`
*   Setup for PostgreSQL, Redis, Celery Worker, web (Django), web frontend (Nginx).

---

### Phase 2: Database Models & Authentication

#### [NEW] `backend/accounts/`
*   Custom User model supporting roles: `Donor`, `Campaign Owner`, `Admin`.
*   JWT Auth + Email Verification workflows.
*   User Profiles.

#### [NEW] `backend/campaigns/`
*   `Campaign` and `Category` models (Title, Story, Images, Target, End Date, Location, Status).
*   Signals & Celery tasks for updating status automatically.

#### [NEW] `backend/donations/`
*   `Donation` model (linking Donor -> Campaign).
*   Handling anonymous preferences and donation messages.

#### [NEW] `backend/payments/`
*   `Transaction` model tracking gateway responses and verification statuses.
*   Integration points for the payment gateway.

---

### Phase 3: Business Logic & API (DRF)

#### [NEW] `backend/api/`
*   Comprehensive REST API covering:
    *   Auth (`/api/auth/login`, `/api/auth/register`)
    *   Campaigns (`/api/campaigns/`, `/api/campaigns/<id>/`)
    *   Donations (`/api/donations/`)
    *   User Profiles (`/api/users/me/`)

---

### Phase 4: Frontend Templates (Django + Bootstrap)

#### [NEW] `backend/templates/` & `backend/static/`
*   **Base Layouts:** Navbar, Footer, Alerts.
*   **Pages:** Home (Trending/Featured), Campaign Details, Checkout Modal, Dashboard.
*   **Admin Customization:** Replacing Django's default admin with custom analytics views.

---

### Phase 5: Payment Gateway & Celery Integration

*   Integrating **Stripe** (recommended for global reach and ease of testing) to handle generic checkout flows.
*   Configuring Celery for asynchronous confirmation emails and automated cleanup.

---

### Phase 6: Production Readiness

*   `requirements/base.txt`, `requirements/production.txt`.
*   Gunicorn entrypoints.
*   Nginx configuration for static/media routing and reverse proxying to Gunicorn.

## Open Questions

> [!IMPORTANT]
> 1.  **Frontend Strategy:** The prompt mentions "Django Templates + Bootstrap OR React frontend". Because building a full React SPA *and* a Django Template webapp concurrently adds significant duplication, I plan to build the **Django Templates + Bootstrap** frontend while providing a complete **REST API** side-by-side. Is this acceptable?
> 2.  **Payment Gateway:** I propose using **Stripe** for payments as it has robust developer tools and sandbox environments. Should I proceed with Stripe, or do you strictly prefer Razorpay?
> 3.  **Social Login:** Do you want Google OAuth implemented in the first iteration, or prioritized after core functionality?

## Verification Plan

### Automated Tests
*   `python manage.py test` to run Django unit tests for core models and views.
*   API endpoint validation using `pytest-django`.

### Manual Verification
*   Docker Compose full system boot (`docker-compose up`).
*   Manual flow test: User Registration -> Email Verification -> Login -> Create Campaign -> Make Donation (Test Mode) -> View Admin Dashboard.
