"""
Apply migration: add edited/edited_at/deleted/deleted_at to chat_messages if missing.

Usage:
  python apply_chat_migration.py

Reads DB connection info from environment:
  MYSQL_USER / APP_DB_USER  (user)
  MYSQL_PASSWORD / APP_DB_PASSWORD
  MYSQL_DATABASE / TARGET_DB
  DB_HOST (default 127.0.0.1)
  DB_PORT (default 3306)
"""
import os
import sys

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("MYSQL_USER", os.getenv("APP_DB_USER", "language_school_user"))
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", os.getenv("APP_DB_PASSWORD", "change_me"))
DB_NAME = os.getenv("MYSQL_DATABASE", os.getenv("TARGET_DB", "language_school_db"))

# Column definitions to ensure
COLUMNS = [
    ("edited", "TINYINT(1) NOT NULL DEFAULT 0"),
    ("edited_at", "TIMESTAMP NULL DEFAULT NULL"),
    ("deleted", "TINYINT(1) NOT NULL DEFAULT 0"),
    ("deleted_at", "TIMESTAMP NULL DEFAULT NULL"),
]

def try_import_connector():
    try:
        import mysql.connector as mysql_connector
        return "mysql-connector", mysql_connector
    except Exception:
        try:
            import pymysql as pymysql
            return "pymysql", pymysql
        except Exception:
            return None, None

def column_exists(cursor, schema, table, column):
    q = """
        SELECT COUNT(*) AS cnt
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s
    """
    cursor.execute(q, (schema, table, column))
    return cursor.fetchone()[0] > 0

def main():
    name, mod = try_import_connector()
    if mod is None:
        print("No MySQL client library found. Install mysql-connector-python or pymysql.")
        sys.exit(1)

    print(f"Connecting to {DB_HOST}:{DB_PORT} database '{DB_NAME}' as '{DB_USER}' using {name}...")
    try:
        if name == "mysql-connector":
            conn = mod.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
            cursor = conn.cursor()
        else:
            conn = mod.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, autocommit=False)
            cursor = conn.cursor()
    except Exception as e:
        print("Failed to connect:", e)
        sys.exit(1)

    try:
        table = "chat_messages"
        changed = False
        for col_name, col_def in COLUMNS:
            try:
                if column_exists(cursor, DB_NAME, table, col_name):
                    print(f"Column '{col_name}' already exists, skipping.")
                    continue
            except Exception:
                # If information_schema access fails, attempt to ALTER and ignore errors
                print("Warning: could not inspect information_schema; will attempt ALTER and ignore errors.")

            alter_sql = f"ALTER TABLE `{table}` ADD COLUMN `{col_name}` {col_def};"
            try:
                cursor.execute(alter_sql)
                print(f"Added column '{col_name}'.")
                changed = True
            except Exception as ex:
                # If column exists concurrently or server doesn't support the exact syntax, report and continue
                print(f"Could not add column '{col_name}': {ex}")
        if changed:
            try:
                conn.commit()
            except Exception:
                pass
            print("Migration applied (some columns added).")
        else:
            print("No changes required.")
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
