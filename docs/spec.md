# Invoice Management Application - Technical Specification

## Project Overview

A modern web application for generating and managing professional invoices with multi-user support, authentication, PDF generation, email delivery, and analytics capabilities.

## Technology Requirements

### Package Management
- Use **uv** for Python package management. 
- Make sure to use virtual environment so that the installed packages are isolated from the system.
- Use lock file to ensure the dependencies are the same across all environments.

### Backend Framework
- Free choice of Python web framework (e.g., Flask, FastAPI, Django, etc.)
- The AI should select the most appropriate framework based on project requirements

### Database
- **PostgreSQL** for both local development and production environments
- Implement proper connection pooling and keepalive settings
- Database schema should be designed by the AI based on application needs

### Frontend
- Free choice of frontend approach (server-side rendering, SPA, hybrid, etc.)
- AI should select appropriate UI framework, styling solutions, and JavaScript libraries
- Ensure responsive design for mobile and desktop use

### Deployment
- **Docker Compose** for production deployment
- Container orchestration for application and database services

## Core Features

### 1. User Management & Authentication

**Multi-Authentication Support:**
- Email + password authentication with secure password hashing
- Social login integration (Google, X/Twitter, GitHub, etc.)
- User session management and secure authentication flows

**User Profiles:**
- Individual company profiles per user
- Company information: name, contact person, address, phone, email, VAT/tax number
- Configurable default VAT/tax rates
- User-specific data isolation (users can only access their own data)

### 2. Invoice Management

**Invoice Operations:**
- Create, read, update, and delete invoices
- Draft and final invoice statuses
- Auto-generated invoice numbers with customizable format patterns
- Search and filter capabilities:
  - Date range filtering
  - Client/recipient name search
  - Invoice status filtering
  - Invoice number search
- Pagination for invoice lists

**Invoice Data Structure:**
- Company details (sender information, bank account payment details)
- Recipient/client details (name, company, address, email, VAT number, customer number)
- Invoice metadata (number, date, due date)
- Line items with:
  - Description
  - Quantity
  - Unit price
  - Line totals
- Automatic calculations:
  - Subtotal
  - VAT/tax amount
  - Total amount
- Timestamps for creation and updates

### 3. PDF Generation & Preview

**PDF Requirements:**
- Generate professional A4 format invoices
- Clean, professional styling with proper margins
- Include all invoice data:
  - Company and recipient information
  - Invoice number, dates
  - Itemized line items in table format
  - Subtotal, VAT, and total calculations
  
**Critical Requirement:**
- **PDF preview in the application must be pixel-perfect identical to the generated PDF file**
- Users should see exactly what the PDF will look like before generating/sending

### 4. Email Integration

**Email Functionality:**
- Send invoices via email with PDF attachments
- SMTP-based email delivery
- Customizable email templates (HTML format)
- Error handling and delivery status tracking
- Configuration for SMTP server settings

### 5. Analytics & Reporting

**User Activity Tracking:**
- **Google Analytics Integration:**
  - Track website traffic and user behavior
  - Measure user engagement with key features
  - Event tracking for specific actions (e.g., "Invoice Created", "Email Sent")
  - Compliance with privacy regulations (cookie consent, anonymization)

**Analytics Dashboard:**
- Revenue tracking over time
- Invoice status breakdown (draft vs. final, paid vs. unpaid)
- Top clients by revenue
- Monthly/quarterly/yearly revenue summaries
- Average invoice value
- Outstanding invoices and amounts
- Time-based trends and visualizations

**Export Capabilities:**
- Export invoice data for accounting purposes
- Generate summary reports

### 6. Subscription & Payments

**Payment Infrastructure:**
- Integration with modern payment processing (e.g., Stripe)
- Support for recurring subscriptions and one-time payments
- Secure customer portal for billing management

**Paid Features & Limits:**
- **Tiered Plans:**
  - Free Tier: Usage limits (e.g., maximum number of invoices per month)
  - Pro Tier: Unlimited access and premium features
- **Enforcement:**
  - System checks for plan limits before performing actions
  - UI indicators for premium-only features
  - Automated upgrades/downgrades handling

### 7. System Administration

**Admin Role:**
- Special "Admin" user type with system-wide privileges
- Secured admin dashboard separated from the main user interface

**User Management:**
- **Overview:** View all registered users/companies with status and plan details
- **Actions:**
  - Enable or disable (ban) user accounts
  - Initiate password reset process for users
  - Manage user subscription status manually
- **Monitoring:** View aggregate system stats (total users, total invoices, server health)

## Security Requirements

**Data Protection:**
- Secure password hashing (use modern algorithms)
- Protection against common vulnerabilities:
  - SQL injection
  - XSS attacks
  - CSRF protection
  - Open redirect attacks
  - NaN/Infinity injection in numeric inputs
- User data isolation (strict user-specific data access controls)

**Authentication Security:**
- Secure session management
- Token-based authentication for API endpoints (if applicable)
- OAuth 2.0 implementation for social logins
- Secure storage of API keys and secrets

## Backup & Data Management

**Backup Strategy:**
- **Manual backup capability** via command or script
- **Automated backup option** to Amazon S3
  - Configurable backup schedule
  - Retention policy configuration
  - Encrypted backups
- Database backup includes all user data and invoices
- Easy restoration process from backups

## Production Deployment Requirements

**Docker Compose Setup:**
- Multi-container architecture (application, database, etc.)
- Proper container networking
- Volume management for persistent data
- Environment-based configuration
- Health checks for services
- Restart policies for reliability

**Production Considerations:**
- Reverse proxy configuration (nginx, traefik, etc.)
- SSL/TLS certificate management
- Log aggregation and monitoring
- Scalability considerations
- Database connection pooling

## Development Environment

**Local Development:**
- PostgreSQL database (same as production)
- Hot-reload/auto-restart during development
- Debug logging and error messages
- Seed data or fixtures for testing
- Database migration management

## Performance & Quality Requirements

- Fast page load times
- Efficient database queries with proper indexing
- Pagination for large datasets
- Responsive UI across devices
- Proper error handling and user feedback
- Input validation (client-side and server-side)
- Clean, maintainable code structure
- Comprehensive logging

## Testing Principles

### General Guidelines
- **Isolation:** Tests must be isolated from external services. No network calls to 3rd party APIs (e.g., Google, Stripe) should be made during testing.
- **Mocking:** Use mocking for all external dependencies.
- **Coverage:** Aim for high test coverage, particularly for critical paths like authentication and billing.

### Issues to Avoid
- **Flaky Tests:** Avoid relying on time.sleep() or external state that can change.
- **External Dependencies:** DO NOT contact real external servers (Google, AWS S3, etc.) in tests. This slows down tests and introduces points of failure.
- **Data Pollution:** Ensure tests clean up after themselves or use transaction rollbacks.

## Deliverables

The implementation should include:

1. Complete application source code
2. Database migration files/scripts
3. Docker Compose configuration for production
4. Documentation:
   - Setup and installation instructions
   - Environment variables reference
   - Backup and restore procedures
   - Development workflow guide
   - API documentation (if applicable)
5. Sample configuration files
6. Scripts for common operations (backup, restore, migrations, etc.)

## Success Criteria

- Users can register, login, and manage their company profiles
- Users can create, edit, and delete invoices
- PDF generation produces professional, accurate invoices
- PDF preview matches generated PDF exactly
- Invoices can be emailed with PDF attachments
- Analytics dashboard provides meaningful insights
- Application runs reliably in Docker containers
- Backups can be created manually and automatically to S3
- All data is properly isolated between users
- Security best practices are implemented throughout
- Admin users can manage user accounts and system status
- Subscription payments and plan limits are correctly handled
- User activity is tracked via Google Analytics