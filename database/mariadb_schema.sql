-- Cyber Guard Phase 1 - MariaDB schema for `cybergaurd_data`
-- Run inside MariaDB after selecting the database:
--   USE cybergaurd_data;

CREATE TABLE IF NOT EXISTS companies (
  company_id      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  company_name    VARCHAR(255) NOT NULL,
  external_org_id VARCHAR(64) NULL,
  status          ENUM('active','inactive') NOT NULL DEFAULT 'active',
  created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME NULL,
  UNIQUE KEY uq_companies_org (external_org_id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS departments (
  department_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  company_id    BIGINT UNSIGNED NOT NULL,
  department_name VARCHAR(255) NOT NULL,
  is_active     TINYINT(1) NOT NULL DEFAULT 1,
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    DATETIME NULL,
  CONSTRAINT fk_departments_company
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
      ON DELETE CASCADE,
  INDEX idx_departments_company (company_id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS users (
  user_id       BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  company_id    BIGINT UNSIGNED NULL,
  department_id BIGINT UNSIGNED NULL,
  role          ENUM('super_admin','client_admin','department_admin','employee') NOT NULL,
  email         VARCHAR(255) NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  full_name     VARCHAR(255) NULL,
  status        ENUM('active','inactive','suspended') NOT NULL DEFAULT 'active',
  last_login    DATETIME NULL,
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    DATETIME NULL,
  UNIQUE KEY uq_users_company_email (company_id, email),
  INDEX idx_users_company (company_id),
  INDEX idx_users_role (role),
  CONSTRAINT fk_users_company
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
      ON DELETE SET NULL,
  CONSTRAINT fk_users_department
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
      ON DELETE SET NULL
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS user_departments (
  user_id       BIGINT UNSIGNED NOT NULL,
  department_id BIGINT UNSIGNED NOT NULL,
  is_default    TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, department_id),
  CONSTRAINT fk_ud_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
      ON DELETE CASCADE,
  CONSTRAINT fk_ud_department
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
      ON DELETE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS endpoints (
  device_id     VARCHAR(64) PRIMARY KEY,
  company_id    BIGINT UNSIGNED NOT NULL,
  department_id BIGINT UNSIGNED NULL,
  user_id       BIGINT UNSIGNED NULL,
  os            VARCHAR(50) NOT NULL,
  ip            VARCHAR(45) NULL,
  status        ENUM('online','offline','decommissioned') NOT NULL DEFAULT 'offline',
  last_seen     DATETIME NULL,
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_endpoints_company (company_id),
  INDEX idx_endpoints_user (user_id),
  CONSTRAINT fk_endpoints_company
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
      ON DELETE CASCADE,
  CONSTRAINT fk_endpoints_department
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
      ON DELETE SET NULL,
  CONSTRAINT fk_endpoints_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
      ON DELETE SET NULL
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS activity_logs (
  log_id      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  device_id   VARCHAR(64) NOT NULL,
  company_id  BIGINT UNSIGNED NOT NULL,
  user_id     BIGINT UNSIGNED NULL,
  timestamp   DATETIME NOT NULL,
  cpu         DECIMAL(5,2) NULL,
  network     DECIMAL(10,2) NULL,
  apps        JSON NULL,
  risk_score  DECIMAL(5,2) NULL,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_activity_company_time (company_id, timestamp),
  INDEX idx_activity_user_time (user_id, timestamp),
  INDEX idx_activity_device_time (device_id, timestamp),
  CONSTRAINT fk_logs_device
    FOREIGN KEY (device_id) REFERENCES endpoints(device_id)
      ON DELETE CASCADE,
  CONSTRAINT fk_logs_company
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
      ON DELETE CASCADE,
  CONSTRAINT fk_logs_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
      ON DELETE SET NULL
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS alerts (
  alert_id    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  type        VARCHAR(64) NOT NULL,
  severity    ENUM('low','medium','high','critical') NOT NULL,
  company_id  BIGINT UNSIGNED NOT NULL,
  device_id   VARCHAR(64) NULL,
  user_id     BIGINT UNSIGNED NULL,
  description TEXT NOT NULL,
  risk_score  DECIMAL(5,2) NULL,
  is_resolved TINYINT(1) NOT NULL DEFAULT 0,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  resolved_at DATETIME NULL,
  resolved_by BIGINT UNSIGNED NULL,
  INDEX idx_alerts_company_time (company_id, created_at),
  INDEX idx_alerts_severity (severity),
  CONSTRAINT fk_alerts_company
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
      ON DELETE CASCADE,
  CONSTRAINT fk_alerts_device
    FOREIGN KEY (device_id) REFERENCES endpoints(device_id)
      ON DELETE SET NULL,
  CONSTRAINT fk_alerts_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
      ON DELETE SET NULL,
  CONSTRAINT fk_alerts_resolved_by
    FOREIGN KEY (resolved_by) REFERENCES users(user_id)
      ON DELETE SET NULL
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;
