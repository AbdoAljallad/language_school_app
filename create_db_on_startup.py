"""
Check for Docker; if Docker is not available and a MySQL server is reachable,
create the target database and an application user.

Environment variables (with defaults):
  DB_ROOT_USER (default: root)
  DB_ROOT_PASSWORD (default: "")
  DB_HOST (default: 127.0.0.1)
  DB_PORT (default: 3306)
  TARGET_DB (default: language_school_db)
  APP_DB_USER (default: language_school_user)
  APP_DB_PASSWORD (default: change_me)

Requires one of:
  pip install mysql-connector-python
  or
  pip install pymysql

Usage: python create_db_on_startup.py
"""
import os
import socket
import subprocess
import sys
import time

DB_ROOT_USER = os.getenv("DB_ROOT_USER", "root")
DB_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", os.getenv("DB_ROOT_PASSWORD", ""))
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
TARGET_DB = os.getenv("MYSQL_DATABASE", os.getenv("TARGET_DB", "language_school_db"))
APP_DB_USER = os.getenv("MYSQL_USER", os.getenv("APP_DB_USER", "language_school_user"))
APP_DB_PASSWORD = os.getenv("MYSQL_PASSWORD", os.getenv("APP_DB_PASSWORD", "change_me"))

def docker_available():
    try:
        res = subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
        return res.returncode == 0
    except Exception:
        return False

def mysql_port_open(host, port, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def try_import_connectors():
    try:
        import mysql.connector as mysql_connector
        return "mysql-connector", mysql_connector
    except Exception:
        try:
            import pymysql as pymysql
            return "pymysql", pymysql
        except Exception:
            return None, None

def create_db_with_mysql_connector(mysql_connector):
    conn = mysql_connector.connect(host=DB_HOST, port=DB_PORT, user=DB_ROOT_USER, password=DB_ROOT_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{TARGET_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    )
    # create user for any host (same as Docker) and also for localhost to cover local clients
    cursor.execute(
        f"CREATE USER IF NOT EXISTS '{APP_DB_USER}'@'%' IDENTIFIED BY %s;", (APP_DB_PASSWORD,)
    )
    try:
        cursor.execute(
            f"CREATE USER IF NOT EXISTS '{APP_DB_USER}'@'localhost' IDENTIFIED BY %s;", (APP_DB_PASSWORD,)
        )
    except Exception:
        # some MySQL versions may already have the user or not support duplicate creation; ignore
        pass
    cursor.execute(f"GRANT ALL PRIVILEGES ON `{TARGET_DB}`.* TO '{APP_DB_USER}'@'%';")
    cursor.execute(f"GRANT ALL PRIVILEGES ON `{TARGET_DB}`.* TO '{APP_DB_USER}'@'localhost';")
    cursor.execute("FLUSH PRIVILEGES;")
    conn.commit()
    cursor.close()
    conn.close()

def create_db_with_pymysql(pymysql):
    conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_ROOT_USER, password=DB_ROOT_PASSWORD, autocommit=True)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{TARGET_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    # create user for any host (Docker-like) and also try localhost
    try:
        cursor.execute(f"CREATE USER '{APP_DB_USER}'@'%' IDENTIFIED BY %s;", (APP_DB_PASSWORD,))
    except Exception:
        pass
    try:
        cursor.execute(f"CREATE USER '{APP_DB_USER}'@'localhost' IDENTIFIED BY %s;", (APP_DB_PASSWORD,))
    except Exception:
        pass
    cursor.execute(f"GRANT ALL PRIVILEGES ON `{TARGET_DB}`.* TO '{APP_DB_USER}'@'%';")
    cursor.execute(f"GRANT ALL PRIVILEGES ON `{TARGET_DB}`.* TO '{APP_DB_USER}'@'localhost';")
    cursor.execute("FLUSH PRIVILEGES;")
    cursor.close()
    conn.close()

def main():
    if docker_available():
        print("Docker is available. Skipping local DB creation.")
        return

    print("Docker not found. Checking for MySQL on {}:{}...".format(DB_HOST, DB_PORT))
    if not mysql_port_open(DB_HOST, DB_PORT):
        print("No MySQL service detected at {}:{}. Cannot create local database.".format(DB_HOST, DB_PORT))
        return

    connector_name, module = try_import_connectors()
    if module is None:
        print("No MySQL client library found. Install one of:")
        print("  pip install mysql-connector-python")
        print("or")
        print("  pip install pymysql")
        return

    try:
        if connector_name == "mysql-connector":
            create_db_with_mysql_connector(module)
        else:
            create_db_with_pymysql(module)
        print(f"Database '{TARGET_DB}' and user '{APP_DB_USER}' have been created or verified.")
    except Exception as ex:
        print("Failed to create database or user. Error:")
        print(str(ex))
        print("Ensure the root credentials are correct and have sufficient privileges, or set DB_ROOT_PASSWORD environment variable.")

if __name__ == "__main__":
    main()
