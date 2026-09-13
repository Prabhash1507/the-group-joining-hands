"""
The Group of Joining Hands - Configuration Module
=================================================
Enterprise System Configuration Parameters
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env file manually if it exists to populate os.environ
_env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(_env_path):
    with open(_env_path, 'r', encoding='utf-8') as _f:
        for _line in _f:
            _line = _line.strip()
            if not _line or _line.startswith('#'):
                continue
            if '=' in _line:
                _key, _val = _line.split('=', 1)
                _key = _key.strip()
                _val = _val.strip()
                if (_val.startswith('"') and _val.endswith('"')) or (_val.startswith("'") and _val.endswith("'")):
                    _val = _val[1:-1]
                # Only set if not already set by system env to preserve overrides
                if _key not in os.environ:
                    os.environ[_key] = _val

# Environment and Network Binding
APP_ENV = os.environ.get('APP_ENV', 'development').lower()
PORT = int(os.environ.get('PORT', '8080'))
HOST = os.environ.get('HOST', '0.0.0.0')

# Security Secrets (Configurable via ENV, with secure fallback in dev)
SECRET_KEY = os.environ.get('SECRET_KEY', 'jh-enterprise-secret-key-prod-change-in-env-2026')
JWT_SECRET = os.environ.get('JWT_SECRET', 'jh-enterprise-jwt-token-secret-2026')

# Allowed CORS Origins (Comma-separated in env, default allows localhost in dev)
ALLOWED_ORIGINS_RAW = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:8080,http://127.0.0.1:8080')
ALLOWED_ORIGINS = [o.strip() for o in ALLOWED_ORIGINS_RAW.split(',') if o.strip()]

# Database Abstraction & Provider Configuration (SQLite default; PostgreSQL migration ready)
DB_PROVIDER = os.environ.get('DB_PROVIDER', 'sqlite').lower()
DATABASE_URL = os.environ.get('DATABASE_URL', '') # Used when DB_PROVIDER=postgresql

# Database Paths for SQLite
DB_DIR = os.path.join(BASE_DIR, 'database')
_db_file_raw = os.environ.get('DB_FILE', os.path.join(DB_DIR, 'database.db'))
DB_FILE = _db_file_raw if os.path.isabs(_db_file_raw) else os.path.abspath(os.path.join(BASE_DIR, _db_file_raw))

_backup_dir_raw = os.environ.get('BACKUP_DIR', os.path.join(DB_DIR, 'backups'))
BACKUP_DIR = _backup_dir_raw if os.path.isabs(_backup_dir_raw) else os.path.abspath(os.path.join(BASE_DIR, _backup_dir_raw))

# Storage Backend Configuration (local | s3 | cloud)
STORAGE_BACKEND = os.environ.get('STORAGE_BACKEND', 'local').lower()

STATIC_DIR = os.path.join(BASE_DIR, 'static')
CSS_DIR = os.path.join(STATIC_DIR, 'css')
JS_DIR = os.path.join(STATIC_DIR, 'js')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
UPLOADS_DIR = os.path.join(STATIC_DIR, 'uploads')

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
INDEX_HTML_PATH = os.path.join(TEMPLATES_DIR, 'index.html')

LOGS_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOGS_DIR, 'audit.log')

# Ensure directories exist
for path in [DB_DIR, BACKUP_DIR, STATIC_DIR, CSS_DIR, JS_DIR, IMAGES_DIR, UPLOADS_DIR, TEMPLATES_DIR, LOGS_DIR]:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

