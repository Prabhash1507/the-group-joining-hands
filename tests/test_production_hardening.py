"""
The Group of Joining Hands - Production Hardening & Infrastructure Tests
========================================================================
Validates the 4 Safe Production Hardening Upgrades:
1. Migration-Ready Database Abstraction
2. Persistent Media Storage Layer
3. Backup Creation, Integrity Verification & Non-Destructive Restore
4. Production Configuration & Secrets Isolation
"""

import unittest
import os
import shutil
import tempfile
import sqlite3

from app.config.config import BASE_DIR, SECRET_KEY, JWT_SECRET, STORAGE_BACKEND, DB_PROVIDER
from app.database.db import get_db, init_db, backup_db, restore_db, verify_backup_integrity
from app.helpers.storage import storage, LocalMediaStorage, get_storage_backend

class TestProductionHardening(unittest.TestCase):
    
    def setUp(self):
        # Create an isolated temporary test directory
        self.test_dir = tempfile.mkdtemp(prefix="jh_prod_hardening_")
        self.test_db = os.path.join(self.test_dir, "test_target.db")
        self.test_backup = os.path.join(self.test_dir, "test_backup.db")
        self.test_uploads = os.path.join(self.test_dir, "uploads")
        os.makedirs(self.test_uploads, exist_ok=True)
        
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    # -------------------------------------------------------------
    # 1. Database Abstraction & Migration-Readiness
    # -------------------------------------------------------------
    def test_01_database_provider_configuration(self):
        """Verify database provider default is SQLite and migration-ready config exists."""
        self.assertIn(DB_PROVIDER, ['sqlite', 'postgresql'])
        conn = get_db()
        self.assertIsNotNone(conn)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys")
        fk_status = cursor.fetchone()[0]
        self.assertEqual(fk_status, 1, "Foreign key cascades must be enabled")
        conn.close()

    def test_02_database_schema_integrity(self):
        """Verify all essential tables exist and schema is intact."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {r[0] for r in cursor.fetchall()}
        required = {'users', 'posts', 'connections', 'direct_messages', 'notifications', 'hashtags', 'events'}
        self.assertTrue(required.issubset(tables), f"Missing required tables: {required - tables}")
        conn.close()

    # -------------------------------------------------------------
    # 2. Persistent Media Storage Layer
    # -------------------------------------------------------------
    def test_03_storage_backend_abstraction(self):
        """Verify storage layer saves, verifies, and retrieves file paths seamlessly."""
        custom_storage = LocalMediaStorage(base_dir=self.test_uploads)
        sample_bytes = b"PNG_MAGIC_BYTES_TEST_PAYLOAD"
        
        saved_path = custom_storage.save(sample_bytes, prefix="test_post", ext=".png")
        self.assertTrue(saved_path.startswith("uploads/test_post_"))
        
        filename = os.path.basename(saved_path)
        self.assertTrue(custom_storage.exists(filename))
        
        full_path = custom_storage.get_path(filename)
        self.assertTrue(os.path.exists(full_path))
        with open(full_path, "rb") as f:
            self.assertEqual(f.read(), sample_bytes)

    # -------------------------------------------------------------
    # 3. Backup, Verification & Non-Destructive Restore
    # -------------------------------------------------------------
    def test_04_backup_creation_and_integrity_verification(self):
        """Verify live backup creation and non-destructive integrity check."""
        backup_file = backup_db(custom_target_path=self.test_backup)
        self.assertIsNotNone(backup_file)
        self.assertTrue(os.path.exists(backup_file))
        
        # Verify backup integrity
        is_valid = verify_backup_integrity(backup_file)
        self.assertTrue(is_valid, "Created backup must pass PRAGMA integrity check and schema validation")

    def test_05_tested_restore_without_overwriting_production(self):
        """Test restore workflow on an isolated test database with full verification."""
        # 1. Create a backup of the current state
        backup_file = backup_db(custom_target_path=self.test_backup)
        self.assertTrue(os.path.exists(backup_file))
        
        # 2. Restore into an isolated temporary database path
        restore_success = restore_db(backup_file, target_db_file=self.test_db)
        self.assertTrue(restore_success)
        self.assertTrue(os.path.exists(self.test_db))
        
        # 3. Verify restored database has intact records
        test_conn = sqlite3.connect(self.test_db)
        test_cursor = test_conn.cursor()
        test_cursor.execute("SELECT COUNT(*) FROM users")
        user_count = test_cursor.fetchone()[0]
        self.assertGreater(user_count, 0, "Restored database must contain seed and registered users")
        
        test_cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        table_count = test_cursor.fetchone()[0]
        self.assertGreaterEqual(table_count, 15, "Restored database must contain all system tables")
        test_conn.close()

    # -------------------------------------------------------------
    # 4. Production Secrets & Configuration
    # -------------------------------------------------------------
    def test_06_secrets_configuration(self):
        """Verify secrets are decoupled and env template exists."""
        self.assertIsNotNone(SECRET_KEY)
        self.assertIsNotNone(JWT_SECRET)
        
        env_example = os.path.join(BASE_DIR, ".env.example")
        self.assertTrue(os.path.exists(env_example), ".env.example must exist in project root")
        with open(env_example, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("SECRET_KEY", content)
            self.assertIn("JWT_SECRET", content)
            self.assertIn("DB_PROVIDER", content)
            self.assertIn("STORAGE_BACKEND", content)


if __name__ == '__main__':
    unittest.main()
