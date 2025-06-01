"""
Database Utility
---------------
Provides functions for connecting to the database and executing queries.
"""

import os
import sys
from dotenv import load_dotenv

# Try to import mysql.connector, provide helpful error if not installed
try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    print("Error: mysql-connector-python package is not installed.")
    print("Please install it using one of the following commands:")
    print("  pip install mysql-connector-python")
    print("  pip install -r requirements.txt")
    print("\nExiting application.")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'rootpassword'),
    'database': os.getenv('DB_NAME', 'language_school'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'auth_plugin': 'mysql_native_password'
}

def get_connection():
    """
    Create and return a connection to the database.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection object
        or None if connection fails.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
    return None

def execute_query(query, params=None, fetch=False, commit=False, many=False):
    """
    Execute a SQL query.
    
    Args:
        query (str): SQL query to execute.
        params (tuple, list, dict, optional): Parameters for the query.
        fetch (bool, optional): Whether to fetch results. Defaults to False.
        commit (bool, optional): Whether to commit the transaction. Defaults to False.
        many (bool, optional): Whether to execute many statements. Defaults to False.
    
    Returns:
        list, dict, int: Query results, or number of affected rows, or None if error.
    """
    connection = get_connection()
    if not connection:
        return None
    
    cursor = None
    result = None
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        if many and params:
            cursor.executemany(query, params)
        elif params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
        else:
            result = cursor.rowcount
        
        if commit:
            connection.commit()
            
    except Error as e:
        print(f"Error executing query: {e}")
        if commit:
            connection.rollback()
        result = None
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()
    
    return result

def execute_transaction(queries):
    """
    Execute multiple queries as a transaction.
    
    Args:
        queries (list): List of dictionaries with 'query' and 'params' keys.
    
    Returns:
        bool: True if transaction succeeded, False otherwise.
    """
    connection = get_connection()
    if not connection:
        return False
    
    cursor = None
    success = False
    
    try:
        cursor = connection.cursor(dictionary=True)
        connection.start_transaction()
        
        for query_dict in queries:
            query = query_dict.get('query')
            params = query_dict.get('params')
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
        
        connection.commit()
        success = True
    except Error as e:
        print(f"Error executing transaction: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()
    
    return success

def initialize_database():
    """
    Initialize the database by creating tables if they don't exist.
    
    Returns:
        bool: True if initialization succeeded, False otherwise.
    """
    connection = get_connection()
    if not connection:
        return False
    
    cursor = None
    success = False
    
    try:
        cursor = connection.cursor()
        
        # Check if the database exists
        cursor.execute("SHOW DATABASES LIKE %s", (DB_CONFIG['database'],))
        database_exists = cursor.fetchone() is not None
        
        if not database_exists:
            # Create the database
            cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
            cursor.execute(f"USE {DB_CONFIG['database']}")
            
            # Read and execute the initialization script
            script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                      'database', 'init.sql')
            
            with open(script_path, 'r') as f:
                sql_script = f.read()
                
            # Split the script into individual statements
            statements = sql_script.split(';')
            
            for statement in statements:
                if statement.strip():
                    cursor.execute(statement)
            
            connection.commit()
            print("Database initialized successfully.")
        else:
            print("Database already exists.")
        
        success = True
    except Error as e:
        print(f"Error initializing database: {e}")
        if connection.is_connected():
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()
    
    return success

class Database:
    """
    Database utility class that provides methods for executing queries.
    """
    
    def fetch_all(self, query, params=None):
        """
        Execute a query and fetch all results.
        
        Args:
            query (str): SQL query to execute.
            params (tuple, list, dict, optional): Parameters for the query.
            
        Returns:
            list: Query results, or None if error.
        """
        return execute_query(query, params, fetch=True)
    
    def fetch_one(self, query, params=None):
        """
        Execute a query and fetch the first result.
        
        Args:
            query (str): SQL query to execute.
            params (tuple, list, dict, optional): Parameters for the query.
            
        Returns:
            dict: Query result, or None if error.
        """
        results = execute_query(query, params, fetch=True)
        if results and len(results) > 0:
            return results[0]
        return None

def database():
    """
    Get a Database utility object.
    
    Returns:
        Database: A Database utility object.
    """
    return Database()

if __name__ == "__main__":
    # Test the database connection
    conn = get_connection()
    if conn:
        print("Successfully connected to the database.")
        conn.close()
    else:
        print("Failed to connect to the database.")