 
 # 🛡️ CyberKeylogger Professional
 
 > A cross‑platform, privacy‑aware, enterprise‑grade monitoring suite for **defensive security**, user awareness, and compliance analytics.
 
 ⚠️ **Legal & Ethical Notice**  
 This project is intended **only** for:
 - Security research and blue‑team simulations
 - Corporate environments where users have been **properly informed** and have **given consent**
 - Environments where monitoring is **explicitly allowed by law and policy**
 
 **Do not** deploy this software for covert or illegal surveillance. You are solely responsible for complying with local laws, organizational policies, and data‑protection regulations.
 
 ---
 
 ## 📚 Table of Contents
 
 1. [Overview](#-overview)
 2. [Key Features](#-key-features)
 3. [Architecture](#-architecture)
 4. [Directory Structure](#-directory-structure)
 5. [Getting Started](#-getting-started)
 6. [Configuration](#-configuration)
 7. [Running the Application](#-running-the-application)
 8. [Security & Privacy by Design](#-security--privacy-by-design)
 9. [Extensibility & Integrations](#-extensibility--integrations)
 10. [Development Notes](#-development-notes)
 11. [License](#-license)
 
 ---
 
 ## 🌐 Overview
 
 CyberKeylogger Professional is a **multi‑component monitoring platform** designed for:
 
 - **Endpoint activity visibility** (keystrokes, clipboard, mouse, screens)
 - **Behavior analytics & anomaly detection**
 - **Administrator dashboards** for security & compliance teams
 - **Audit‑ready logging** with strong cryptography
 
 The system combines **low‑level endpoint monitoring** with a **web dashboard** so that security teams can analyze user activity, detect suspicious behavior, and generate reports – while still respecting **consent, privacy, and transparency**.
 
 ---
 
 ## ✨ Key Features
 
 - **Multi‑channel logging**
   - ⌨️ Keystrokes with active window / application context
   - 📋 Clipboard events with hashed & encrypted content
   - 🖱️ Mouse events with coordinates and window titles
   - 🖼️ Screen captures for high‑risk actions (via `screen_capture`)
 
 - **Dashboard & Web UI**
   - 🔐 Login & role‑based access (admin / employee)
   - 📊 Overview of active employees, keystrokes, and alerts
   - 🚨 Alerts & reports views for quick triage
 
 - **Data Protection**
   - 🔒 AES‑based encryption for sensitive fields
   - 🧾 Structured audit trail stored in SQLite (and optional MariaDB schema)
   - 🧩 Pseudonymization support via encrypted columns
 
 - **Detection & Analytics (Foundation)**
   - 🧠 Anomaly detection hooks
   - 🧨 Script / macro detector
   - 🛡️ Anti‑keylogger / tamper‑detection utilities
 
 - **Cross‑Platform Support (Core Agent)**
   - Windows / macOS / Linux handling inside the logging modules
   - Unified abstraction for app/window context
 
 ---
 
 ## 🧩 Architecture
 
 At a high level, the system is composed of:
 
 - **Core Monitoring Layer (`core/`)**  
   Background services responsible for collecting endpoint signals:
   - `keylogger.py` – hooks keyboard events and attaches active window metadata.
   - `mouse_logger.py` – tracks mouse clicks and movements.
   - `clipboard_logger.py` – captures clipboard changes.
   - `screen_capture.py` – captures screenshots based on triggers.
   - `app_tracker.py` – resolves active application and window information.
 
 - **Data & Persistence Layer (`database/`, `data/`)**  
   - `models.py` – defines the relational schema (keystrokes, mouse events, alerts, users, etc.).
   - `db_manager.py` – thread‑safe insert and query methods for activity, stats, and alerts.
   - `encryption.py` – AES‑CBC helpers for encrypting and decrypting sensitive fields.
   - `data/logs.db` – default SQLite database (created at runtime if missing).
   - `mariadb_schema.sql` – reference schema for MariaDB deployments.
 
 - **Web Server & Dashboard (`server/`)**  
   - `webapp/` – Flask application with HTML templates and static assets for the dashboard.
   - `auth.py` – authentication, authorization, and session management helpers.
   - `api.py` / routes – REST‑style endpoints for stats, employees, alerts, and reports.
   - `websocket_server.py` – optional real‑time channel using WebSockets.
 
 - **Detection & ML (`detection/`, `ml/`)**  
   - Baseline modules for anomaly detection and script / macro analysis.
   - `ml/model.py`, `ml/train_model.py` – stubs for training and integrating ML models.
 
 - **Local UI (`ui/`)**  
   - Desktop‑style GUI for running the agent locally and visualizing basic status.
 
 - **Tooling / Frontend Build (`package.json`, `vite`)**  
   - Optional Vite‑based frontend tooling for richer dashboards or SPA experiences.
 
 The orchestrator is `main.py`, which:
 
 1. Initializes the database schema.
 2. Starts the core logging services (keyboard, mouse, clipboard, etc.).
 3. Boots the Flask web application for the dashboard.
 
 ---
 
 ## 📁 Directory Structure
 
 High‑level layout (simplified):
 
 ```text
 CyberKeylogger/
 ├── core/                 # Endpoint monitoring services (keylogger, mouse, clipboard, screen)
 ├── database/             # DB models, manager, and encryption utilities
 ├── detection/            # Anomaly, anti-keylogger, and script detection modules
 ├── ml/                   # ML utilities and training scripts (optional / experimental)
 ├── server/
 │   ├── webapp/           # Flask app: routes, templates, static assets
 │   ├── api.py            # API endpoints (REST/JSON)
 │   └── auth.py           # Authentication and authorization helpers
 ├── ui/                   # Desktop UI and widgets
 ├── config/               # Configuration files (YAML, keyword lists, etc.)
 ├── data/                 # Runtime data (SQLite DB, exported logs, etc.)
 ├── tests/                # Automated tests and fixtures
 ├── assets/               # Images and static resources
 ├── main.py               # Application entrypoint (starts agents + web server)
 ├── requirements*.txt     # Python dependency sets per OS
 ├── package.json          # Frontend/tooling dependencies (Vite, Chart.js, Axios)
 └── README.md             # You are here
 ```
 
 ---
 
 ## 🚀 Getting Started
 
 ### ✅ Prerequisites
 
 - **Python**: 3.x (3.9+ recommended)
 - **Pip**: Python package manager
 - **Virtualenv** (optional but recommended)
 - **Node.js (optional)**: for running the Vite dev server / frontend tooling
 
 > On Linux you may also need additional packages / permissions for low‑level keyboard and mouse hooks depending on your desktop environment.
 
 ### 🧱 Clone & Setup
 
 ```bash
 git clone <your-repo-url>.git
 cd CyberKeylogger
 ```
 
 Create and activate a virtual environment (recommended):
 
 ```bash
 python3 -m venv .venv
 source .venv/bin/activate
 ```
 
 Install Python dependencies (Linux profile):
 
 ```bash
 pip install -r requirements.txt
 ```
 
 For other platforms:
 
 - Windows: `pip install -r requirements-windows.txt`
 - macOS: `pip install -r requirements-macos.txt`
 
 > These files define OS‑specific packages for screen capture, keyboard hooks, etc.
 
 ---
 
 ## ⚙️ Configuration
 
 Configuration is designed to be **environment‑driven** and **file‑driven**:
 
 - **Config files (`config/`)**
   - YAML / text configuration for:
     - Logging intervals and retention
     - Keyword lists / high‑risk phrases
     - Alert thresholds and severity levels
 
 - **Environment variables (recommended)**
   - Database location / connection details
   - Encryption passwords / keys
   - Secret tokens for web sessions and JWTs
 
 > This README intentionally **does not** document any specific credential values.  
 > Use environment variables or secrets management in your deployment pipeline instead of hardcoding sensitive data.
 
 ---
 
 ## ▶️ Running the Application
 
 From the project root (with virtualenv activated):
 
 ```bash
 python3 main.py
 ```
 
 What happens:
 
 1. The SQLite database (e.g. `data/logs.db`) is created if it does not exist.
 2. Database tables are initialized via `DatabaseModels`.
 3. Keyboard, mouse, and clipboard loggers start in the background.
 4. The Flask web server starts (by default on a local port, configured in `main.py`).
 
 Then open your browser and navigate to the local dashboard URL printed in the console (e.g. `http://127.0.0.1:<port>`).
 
 > **Important:** Default credentials and secrets are **not** listed here by design.  
 > Check your own database seed / admin provisioning process and change any default passwords immediately.
 
 ### 🌐 Optional: Frontend Dev Server (Vite)
 
 If you want to work on the frontend or integrate charts and SPA features:
 
 ```bash
 # From the project root
 npm install      # install JS dependencies (Vite, Chart.js, Axios, ...)
 npm run dev      # start the Vite dev server
 ```
 
 You can then proxy or point the frontend to your running Flask backend.
 
 ---
 
 ## 🔐 Security & Privacy by Design
 
 CyberKeylogger emphasizes **defensive monitoring** and **compliance**:
 
 - **Consent & Transparency**
   - Ensure users are informed that monitoring is enabled.
   - Provide clear policies and onboarding materials.
 
 - **Data Minimization**
   - Only collect data that is necessary for your security or compliance use case.
   - Use filtering and whitelists/blacklists to avoid over‑collection where possible.
 
 - **Encryption & Pseudonymization**
   - Sensitive payloads (e.g. keystroke details, clipboard content) can be encrypted at rest.
   - Pseudonymization can restrict direct access to PII unless strictly required.
 
 - **Access Control**
   - Enforce role‑based access for administrators vs. regular employees.
   - Protect dashboards with strong authentication, HTTPS, and network controls.
 
 - **Audit & Compliance**
   - Maintain logs of admin actions and alert handling.
   - Align retention / deletion policies with frameworks like GDPR, HIPAA, PCI DSS, or NIST guidelines.
 
 > Always involve your legal and compliance teams before deploying monitoring in production.
 
 ---
 
 ## 🧩 Extensibility & Integrations
 
 The codebase is structured for extension:
 
 - **Add new data sources**
   - Implement new loggers in `core/` (e.g. network traffic, USB devices) and wire them into `DBManager`.
 
 - **SIEM / SOAR Integration**
   - Build integrations in `server/integration.py` or dedicated modules to push summarized events to:
     - SIEM platforms (Splunk, ELK/Opensearch, etc.)
     - SOAR / incident response pipelines
 
 - **ML‑based Detection**
   - Use `ml/` utilities to train models on historical data.
   - Plug inference into `detection/` modules to raise smarter alerts.
 
 ---
 
 ## 🛠 Development Notes
 
 - **Code Style & Layout**  
   Standard Python modules with a clear separation between:
   - Monitoring (`core/`)
   - Persistence (`database/`)
   - Presentation (`server/webapp/`, `ui/`)
 
 - **Testing**
   - Automated tests live under `tests/` and `test_*.py` files.
   - You can run your preferred test runner (e.g. `pytest`) from the project root.
 
 - **Cross‑Platform Considerations**
   - Low‑level hooks depend on OS APIs; some features may require additional privileges or libraries on specific platforms.
 
 Contributions that improve **safety**, **observability**, and **compliance features** are especially welcome.
 
 ---
 
 ## 📄 License
 
 This project is distributed under the terms of the license found in [`LICENSE`](LICENSE).  
 Review the license carefully before using this project in commercial or production environments.
