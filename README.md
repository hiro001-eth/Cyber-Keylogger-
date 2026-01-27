# SnapVault - Professional Photo & Video Storage

## Overview

SnapVault is a full-stack web application for photographers and videographers to securely store, organize, and share high-quality photos and videos with clients. It provides project-based organization, client-facing galleries, analytics, and tiered storage plans, aiming to be a comprehensive media management solution for professionals.

This `README.md` gives a high-level overview of the project, tech stack, main features, and where to find more detailed documentation. It does **not** contain any secrets such as API keys, tokens, or passwords.

---

## Key Features

- **Secure Authentication & Sessions**  
  Session-based authentication with Replit OAuth and Express sessions.

- **Project-Based Organization**  
  - Create and manage projects for each client or shoot.
  - Store photos and videos per project.
  - Track project status (e.g., Draft / Active / Archived).
  - Control project privacy (Public / Private).
  - Generate share codes for client access.

- **High-Performance File Storage & Uploads**  
  - Multi-file drag-and-drop uploads.  
  - Progress tracking and real-time feedback.  
  - Validation for common image and video formats (up to 500MB per file).  
  - Storage quota management per subscription plan.  
  - Local filesystem storage under an `uploads/` directory.

- **Tiered Plans & Limits**  
  - Multiple subscription tiers (e.g., Free, Standard, Pro, Ultra).  
  - Different storage limits (e.g., from ~15GB to multi-terabyte).  
  - Different project limits (e.g., from a few projects to unlimited).  
  - Automatic handling of plan changes and overages based on business rules.

- **Client Gallery System**  
  - Public, shareable gallery URLs based on share codes.  
  - Optional PIN-protected downloads.  
  - Responsive gallery layout optimized for client viewing.  
  - Optional protection features (e.g., disabling right-click / basic dev tools shortcuts).

- **Analytics & Tracking (for paid plans)**  
  - IP-based unique visitor tracking.  
  - Device and basic client intelligence.  
  - Project-level analytics and conversion tracking.  
  - Geographic distribution of visitors.  
  - Restricted to paid subscription tiers.

- **QR Code Generator System**  
  - Generate QR codes for text, URLs, code snippets, and images.  
  - Tier-based limits and retention rules (e.g., auto-deletion for certain free-tier assets).

- **Download System**  
  - Fast, single-file downloads without additional compression.  
  - Efficient ZIP generation for multi-file downloads.  
  - Visual progress and clear UI feedback.

- **Admin Interface**  
  - Admin-only dashboard for user management, payments, system operations, and analytics.  
  - Restricted to a designated admin account/email.

- **Modern UI/UX**  
  - Dark theme by default.  
  - Mobile-first responsive design.  
  - Smooth navigation, animations, and loading states.  
  - Accessibility-minded UI with consistent components.  
  - Currency shown in NPR using real-time conversion.

---

## System Architecture

SnapVault is structured as a modern, type-safe full-stack application.

### Frontend

- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Routing**: Wouter
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui over Radix UI primitives
- **State Management**: TanStack Query (React Query) for server state
- **Forms & Validation**:
  - React Hook Form for form state
  - Zod for schema validation
- **Uploads UI**:
  - Drag-and-drop
  - Progress indicators
  - Error handling and retry logic

### Backend

- **Runtime**: Node.js
- **Framework**: Express.js
- **Language**: TypeScript with ES modules
- **Authentication**:
  - Replit Auth (OpenID Connect)
  - Passport.js for authentication middleware
- **Sessions**:
  - Express sessions
  - Session store backed by PostgreSQL
- **File Uploads**:
  - Multer for handling `multipart/form-data` uploads
- **API Design**:
  - RESTful JSON endpoints for all core operations
  - Authenticated routes for user dashboards and admin
  - Public routes for client galleries (by share code)

### Database & Storage

- **Database**: PostgreSQL (configured for Neon serverless in typical deployments)
- **ORM**: Drizzle ORM (type-safe queries)
- **Migrations**: Drizzle Kit
- **File Storage**:
  - Files stored on the server filesystem (e.g., `uploads/` directory).  
  - Database stores metadata such as file paths, sizes, ownership, and project linkage.

---

## Recent Highlights

The project has undergone several important fixes and improvements, including:

- **Upload System Fixes**  
  - Corrected API call syntax and authentication handling.  
  - More robust error handling and user-facing error messages.

- **Authentication Flow Verification**  
  - Confirmed end-to-end login and session behavior with cookies.

- **Project Settings & Privacy Controls**  
  - Fixed persistence issues for project privacy and status changes.  
  - Enforced privacy rules for client galleries, including:
    - Public projects: Accessible via gallery URLs.
    - Private projects: Return 403 with a clear "access denied" message.
    - Draft projects: Return 403 indicating the gallery is not yet published.
    - Archived projects: Return 403 indicating the gallery is no longer available.
  - Consistent behavior across gallery-related endpoints such as:
    - `/api/gallery/:shareCode`
    - `/api/gallery/:shareCode/files`
    - `/api/gallery/:shareCode/download-zip`

- **Enhanced AI Support Chatbot**  
  - Case-insensitive keyword handling.  
  - Better intent recognition for pricing, help, account, and technical issues.  
  - Casual conversation support (greetings, thanks, goodbyes).  
  - Fuzzy matching for more natural understanding.  
  - Smarter fallback responses with contextual suggestions.

- **Deployment Scripts v2.0.0**  
  - Fully rebuilt deployment automation with:
    - Production-ready `deploy.sh` script.  
    - Simplified `quick-deploy.sh` for development.  
    - Extensive validation, logging, and rollback handling.

---

## Deployment & Operations

SnapVault includes a robust deployment system designed for both development and production.

### Deployment Scripts

- **`deploy.sh`**  
  Full-featured deployment script for production-ready environments. Handles:
  - System validation (Node.js, npm, PostgreSQL, disk, memory).  
  - Secure configuration and environment setup.  
  - SSL/HTTPS configuration.  
  - Process management with PM2.  
  - Reverse proxy configuration (nginx).  
  - Backup creation and rollback support.  
  - Extensive logging and reporting.

- **`quick-deploy.sh`**  
  Streamlined script for local development or quick setups. Automates many of the same checks with a faster, developer-focused path.

- **`deployment.config.json`**  
  Template(s) for environment-specific deployment configuration.

- **`DEPLOYMENT.md`**  
  Detailed deployment documentation, including troubleshooting and step-by-step instructions.  
  **Refer to `DEPLOYMENT.md` for concrete commands and full deployment flow.**

### Typical Deployment Options

Examples of how the deployment scripts can be used (refer to `DEPLOYMENT.md` for exact options and the most accurate, up-to-date usage):

- Development-style deployments
- Production deployments with SSL and backups
- Test/validation runs that perform checks without making permanent changes

> **Important:** This README intentionally does **not** list any secret values. Actual environment variables and their secure configuration should be managed via `.env` files, secret stores, or your hosting provider, and are documented in more detail in deployment/configuration docs.

---

## Tech Stack Summary

- **Frontend**
  - React 18 + TypeScript
  - Vite
  - Wouter (routing)
  - Tailwind CSS
  - shadcn/ui built on Radix UI primitives
  - TanStack Query
  - React Hook Form + Zod

- **Backend**
  - Node.js + Express.js
  - TypeScript (ES modules)
  - Passport.js + Replit Auth
  - Multer for uploads

- **Data & Storage**
  - PostgreSQL (Neon serverless friendly)
  - Drizzle ORM + Drizzle Kit
  - Local filesystem storage for files (e.g., `uploads/`)

- **Tooling & Ops**
  - Deployment via `deploy.sh` and `quick-deploy.sh`
  - PM2 for process management (production)
  - nginx as reverse proxy (production)

---

## Getting Started (High-Level)

> For exact commands and environment variable details, please see `DEPLOYMENT.md` and the `package.json` scripts in the repository. This section is intentionally high-level and does **not** contain secrets.

### Prerequisites

- Node.js (20+ recommended)
- npm (10+ recommended)
- PostgreSQL (12+ recommended) or a managed instance such as Neon

### High-Level Setup Flow

1. **Clone the repository**
2. **Install dependencies** using npm or your preferred package manager.
3. **Configure environment variables** in a local `.env` file or your deployment environment:  
   Typical values will include items such as:
   - Database connection URL(s)
   - Session secret(s)
   - OAuth / Replit Auth client configuration

   Do **not** commit these secrets to version control.
4. **Initialize the database schema** using Drizzle ORM / Drizzle Kit, following the commands described in `DEPLOYMENT.md`.
5. **Run the application** using the appropriate script from `package.json` (development or production mode).  
   Again, see `DEPLOYMENT.md` and repository scripts for the authoritative commands.

---

## Project Structure (High-Level)

While the exact structure may evolve, a typical layout looks like:

- `frontend/` or `src/` — React application code (components, routes, hooks, styles).
- `server/` or `backend/` — Express/TypeScript backend (routes, controllers, services, models).
- `drizzle/` or `db/` — Database schema and migration files for Drizzle ORM.
- `uploads/` — Filesystem storage for uploaded media (should be ignored in version control and protected in production).
- `scripts/` — Deployment and utility scripts such as `deploy.sh` and `quick-deploy.sh`.
- `DEPLOYMENT.md` — Detailed deployment and configuration guide.

Refer to the repository itself for the precise layout and naming, as some directories may differ.

---

## Security & Privacy Notes

- **Secrets Management**  
  - Secrets (database URLs, API keys, session secrets, OAuth credentials) must not be committed to Git.  
  - Use `.env` files, secret managers, or environment configuration provided by your hosting platform.

- **Access Control**  
  - Authentication and authorization are enforced on sensitive endpoints.  
  - Client galleries use project privacy and status rules to determine access.

- **Data Protection**  
  - Uploaded media is stored on the server filesystem; secure your storage directories with appropriate permissions and access policies.  
  - Consider HTTPS and strong session security for production deployments.

---

## Contributing

If you plan to extend or modify SnapVault:

1. Review the existing architecture and docs (`replit.md`, `DEPLOYMENT.md`, and this `README.md`).
2. Follow the existing coding style (TypeScript on both frontend and backend).
3. Keep security and privacy in mind when handling uploads, authentication, and analytics.
4. Avoid committing any sensitive configuration or user data.

---

## License

The license for this project is not specified in this README. Please refer to the repository or project owner for licensing details.
