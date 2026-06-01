import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    """Database configuration class"""
    
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'hospital_management'),
            'port': int(os.getenv('DB_PORT', 3306))
        }
    
    def get_connection(self):
        """Create and return database connection"""
        try:
            connection = mysql.connector.connect(**self.config)
            return connection
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None