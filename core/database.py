import os
from urllib.parse import urlparse
import dj_database_url
from psycopg2.pool import ThreadedConnectionPool
from django.core.exceptions import ImproperlyConfigured

# Connection pool settings
POOL_MIN_CONN = 1
POOL_MAX_CONN = 20

# Initialize connection pool
connection_pool = None

def get_database_config():
    """Get database configuration without initializing models"""
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ImproperlyConfigured("DATABASE_URL environment variable is not set")

    try:
        config = dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
        # Add additional settings
        config.update({
            'CONN_MAX_AGE': 600,
            'CONN_HEALTH_CHECKS': True,
            'OPTIONS': {
                'sslmode': 'require',
                'connect_timeout': 10,
            }
        })
        return config
    except Exception as e:
        raise ImproperlyConfigured(f"Error configuring database: {str(e)}")

def get_connection_pool():
    """Get or create connection pool"""
    global connection_pool
    if connection_pool is None:
        try:
            DATABASE_URL = os.getenv('DATABASE_URL')
            if not DATABASE_URL:
                raise ImproperlyConfigured("DATABASE_URL environment variable is not set")
                
            db_url = urlparse(DATABASE_URL)
            connection_pool = ThreadedConnectionPool(
                POOL_MIN_CONN,
                POOL_MAX_CONN,
                host=db_url.hostname,
                port=db_url.port,
                database=db_url.path[1:],
                user=db_url.username,
                password=db_url.password,
                sslmode='require'
            )
        except Exception as e:
            raise ImproperlyConfigured(f"Error creating connection pool: {str(e)}")
    return connection_pool

def get_connection():
    """Get a connection from the pool"""
    pool = get_connection_pool()
    try:
        return pool.getconn()
    except Exception as e:
        raise ImproperlyConfigured(f"Error getting connection from pool: {str(e)}")

def release_connection(conn):
    """Release a connection back to the pool"""
    pool = get_connection_pool()
    try:
        pool.putconn(conn)
    except Exception as e:
        raise ImproperlyConfigured(f"Error releasing connection to pool: {str(e)}")

# Database router for connection pooling
class ConnectionPoolRouter:
    def db_for_read(self, model, **hints):
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True 