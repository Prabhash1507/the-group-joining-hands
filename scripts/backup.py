#!/usr/bin/env python
"""
The Group of Joining Hands - Standalone Backup & Verified Restore CLI
=====================================================================
Usage:
    python scripts/backup.py backup               -> Creates a verified timestamped backup
    python scripts/backup.py verify <backup_file> -> Validates backup integrity without restoring
    python scripts/backup.py restore <backup_file> [target_db] -> Restores database safely
"""

import sys
import os

# Add parent directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.db import backup_db, restore_db, verify_backup_integrity

def print_help():
    print("""
Joining Hands Database Backup & Restore Utility
================================================
Commands:
  backup                   Create timestamped backup in database/backups/
  verify <backup_file>     Verify integrity of a backup file
  restore <backup_file>    Restore backup to active database (database/database.db)
""")

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or args[0] in ['-h', '--help', 'help']:
        if not args:
            # Default action: create backup
            print("Starting automated database backup...")
            backup_path = backup_db()
            if backup_path:
                if verify_backup_integrity(backup_path):
                    print(f"SUCCESS: Verified backup created at: {backup_path}")
                else:
                    print(f"WARNING: Backup created but failed integrity check: {backup_path}")
            else:
                print("FAILED: Backup failed or database file missing.")
        else:
            print_help()
    elif args[0] == 'backup':
        target = args[1] if len(args) > 1 else None
        backup_path = backup_db(target)
        if backup_path and verify_backup_integrity(backup_path):
            print(f"SUCCESS: Backup created and verified: {backup_path}")
        else:
            print("FAILED: Backup creation failed.")
    elif args[0] == 'verify':
        if len(args) < 2:
            print("Error: Specify backup file path to verify.")
            sys.exit(1)
        valid = verify_backup_integrity(args[1])
        if valid:
            print(f"SUCCESS: Backup file {args[1]} is 100% valid and verified.")
        else:
            print(f"FAILED: Backup file {args[1]} is corrupted or invalid.")
            sys.exit(1)
    elif args[0] == 'restore':
        if len(args) < 2:
            print("Error: Specify backup file path to restore.")
            sys.exit(1)
        target = args[2] if len(args) > 2 else None
        success = restore_db(args[1], target)
        if success:
            print(f"SUCCESS: Database restored successfully.")
        else:
            print(f"FAILED: Database restoration failed.")
            sys.exit(1)
    else:
        print(f"Unknown command: {args[0]}")
        print_help()
        sys.exit(1)
