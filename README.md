# Invoice Management Application

A modern web application for generating and managing professional invoices with multi-user support, authentication, and PDF generation.

## 🚀 Getting Started

### Prerequisites

- **Docker & Docker Compose**
- **Python 3.10+** (for local backend dev)
- **Node.js 18+** (for local frontend dev)

### Running with Docker

1.  Clone the repository.
2.  Create `.env` files for backend and frontend (see `.env.example`).
3.  Run:
    ```bash
    # Default configuration (backend on 0.0.0.0:8000)
    docker-compose up --build

    # Custom backend port
    BACKEND_PORT=9000 docker-compose up --build

    # Custom backend host and port
    BACKEND_HOST=127.0.0.1 BACKEND_PORT=9000 docker-compose up --build
    ```
4.  Access the app at `http://localhost:5173`.

### Google OAuth Setup

To enable Google Login, you need to configure a project in the Google Cloud Console:

1.  Create a project and configure the OAuth consent screen.
2.  Create OAuth 2.0 Client credentials (Web application).
3.  Add the following **Authorized redirect URI**:
    - `http://localhost:8000/auth/google/callback` (or your configured BACKEND_PORT)
4.  Copy the Client ID and Client Secret into your `backend/.env` file.

### Local Development

#### Backend
```bash
cd backend
uv sync
# Default configuration (0.0.0.0:8000)
uv run python server.py
# Custom port
BACKEND_PORT=9000 uv run python server.py
# Custom host and port
BACKEND_HOST=127.0.0.1 BACKEND_PORT=9000 uv run python server.py
```

#### Frontend
```bash
cd frontend
npm install
# Default connects to http://localhost:8000
npm run dev
# Custom backend URL
VITE_API_URL=http://localhost:9000 npm run dev
```

---

## 🗺️ Roadmap

Based on the [Technical Specification](docs/spec.md), here is the implementation status of the defined features.

### 1. User Management & Authentication
- [x] **Multi-Authentication Support**: Email + Password with Argon2 hashing.
- [x] **Social Login**: Google OAuth integration.
- [x] **User Sessions**: JWT-based secure authentication.
- [x] **User Profiles**: Company details handling.
- [x] **Data Isolation**: Strict user-specific data access.

### 2. Invoice Management
- [x] **Invoice Operations**: Create, Read, Update, Delete (CRUD).
- [x] **Invoice Statuses**: Draft and Final status tracking.
- [x] **Auto-generated Numbers**: Default pattern implementation.
- [ ] **Search & Filter**: Date range, client name, status filtering.
- [ ] **Pagination**: Efficient handling of large invoice lists.
- [x] **Data Structure**: Comprehensive model including line items and metadata.
- [x] **Calculations**: Automatic subtotal, tax, and total computation.

### 3. PDF Generation & Preview
- [x] **PDF Generation**: Professional A4 PDF generation using WeasyPrint.
- [x] **Pixel-Perfect Preview**: Native PDF rendering for exact preview fidelity.

### 4. Email Integration
- [ ] **Email Delivery**: Send invoices via SMTP.
- [ ] **Templates**: Customizable HTML email templates.
- [ ] **Tracking**: Delivery status tracking.

### 5. Analytics & Reporting
- [ ] **Google Analytics**: User activity and event tracking.
- [ ] **Analytics Dashboard**: Revenue tracking, charts, and business insights.
- [ ] **Exports**: Data export functionality.

### 6. Subscription & Payments
- [ ] **Payment Integration**: Stripe/Payment provider integration.
- [ ] **Subscription Plans**: Free vs Pro tiers.
- [ ] **Usage Limits**: Enforcement of plan limits (e.g., invoices per month).

### 7. System Administration
- [ ] **Admin Role**: Special superuser privileges.
- [ ] **User Management**: Admin interface to ban users or reset passwords.
- [ ] **System Monitoring**: Health and stats overview.

### 8. Security Requirements
- [x] **Data Protection**: Secure hashing, SQL injection prevention.
- [x] **Auth Security**: OAuth 2.0 and JWT implementation.
- [ ] **Advanced Security**: CSRF protection (frontend), Rate limiting.

### 9. Backup & Data Management
- [ ] **Manual Backups**: Scripts for on-demand backup.
- [ ] **Automated S3 Backups**: Scheduled backups to cloud storage.

### 10. Production Deployment
- [x] **Docker Compose**: Orchestrated container setup.
- [ ] **Production Tuning**: Reverse proxy (Nginx), SSL, Logging aggregation.
