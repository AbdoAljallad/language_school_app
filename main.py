#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Language School Management System
---------------------------------
Main entry point for the application.
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

# --- Safe DB migration: ensure chat_messages has edited/deleted columns ---
def _try_import_connector():
    try:
        import mysql.connector as mysql_connector
        return "mysql-connector", mysql_connector
    except Exception:
        try:
            import pymysql as pymysql
            return "pymysql", pymysql
        except Exception:
            return None, None

def apply_chat_migration():
    name, mod = _try_import_connector()
    if mod is None:
        print("No MySQL client installed; skipping chat metadata migration.")
        return
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("MYSQL_USER", os.getenv("APP_DB_USER", "root"))
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD", os.getenv("APP_DB_PASSWORD", ""))
    DB_NAME = os.getenv("MYSQL_DATABASE", os.getenv("TARGET_DB", "language_school_db"))
    try:
        if name == "mysql-connector":
            conn = mod.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            cursor = conn.cursor()
        else:
            conn = mod.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            cursor = conn.cursor()
    except Exception as e:
        print("Could not connect to DB for migration:", e)
        return

    cols = [
        ("edited", "TINYINT(1) NOT NULL DEFAULT 0"),
        ("edited_at", "TIMESTAMP NULL DEFAULT NULL"),
        ("deleted", "TINYINT(1) NOT NULL DEFAULT 0"),
        ("deleted_at", "TIMESTAMP NULL DEFAULT NULL"),
    ]
    try:
        # use information_schema when possible
        for col_name, col_def in cols:
            try:
                cursor.execute(
                    "SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND COLUMN_NAME=%s",
                    (DB_NAME, "chat_messages", col_name),
                )
                exists = cursor.fetchone()[0] > 0
            except Exception:
                exists = False
            if exists:
                # already present
                continue
            try:
                sql = f"ALTER TABLE chat_messages ADD COLUMN `{col_name}` {col_def}"
                cursor.execute(sql)
                print(f"Migration: added column {col_name}")
            except Exception as ex:
                # ignore if cannot add (e.g., permissions) but report
                print(f"Migration: could not add {col_name}: {ex}")
        try:
            conn.commit()
        except Exception:
            pass
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

# run migration before importing application modules
apply_chat_migration()

from PyQt5.QtWidgets import QApplication
from app.views.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Initialize and show the main window
    main_window = MainWindow()
    main_window.show()
    
    # Start the application event loop
    sys.exit(app.exec_())