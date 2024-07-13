# db_pool.py
import os
import psycopg2
from psycopg2 import pool
from urllib.parse import urlparse

# Load and parse the database URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

url = urlparse(DATABASE_URL)

# Extract connection parameters from the URL
db_params = {
    'dbname': url.path[1:],
    'user': url.username,
    'password': url.password,
    'host': url.hostname,
    'port': url.port
}

# Log the parameters to ensure they are correctly parsed
print(f"Parsed DB params: {db_params}")

# Ensure all parameters are present
missing_params = [key for key, value in db_params.items() if not value]
if missing_params:
    raise ValueError(f"Missing database connection parameters: {', '.join(missing_params)}")

# Initialize the connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    dbname=db_params['dbname'],
    user=db_params['user'],
    password=db_params['password'],
    host=db_params['host'],
    port=db_params['port']
)

def getconn():
    return connection_pool.getconn()

def putconn(conn):
    connection_pool.putconn(conn)
