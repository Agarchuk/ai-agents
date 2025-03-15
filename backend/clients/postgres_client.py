from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, pool
from backend.config.postgres_config import DB_URL
from utils.logger import log_info, log_error
from sqlalchemy.ext.declarative import declarative_base

# Base class for SQLAlchemy models
Base = declarative_base()

class PostgresClient:
    _instance = None  # Singleton instance

    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the PostgresClient class."""
        if cls._instance is None:
            cls._instance = cls()
            log_info("PostgresClient singleton instance created")
        return cls._instance

    def __init__(self, db_url=None):
        self.db_url = db_url or DB_URL
        self.engine = create_engine(
            self.db_url,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800  # Recycle connections after 30 minutes
        )
        self.Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
        self._connection_disposed = False
        log_info("Postgres client initialized with connection pooling")
        self.create_tables()  # Initialize tables at creation

    def create_tables(self):
        """Create all tables defined in SQLAlchemy models."""
        Base.metadata.create_all(self.engine)
        log_info("Database tables created")

    def close_connection(self):
        if not self._connection_disposed:
            if hasattr(self, 'engine'):
                self.engine.dispose()
                log_info("Database connection disposed")
            else:
                log_info("No database connection to dispose")
            self._connection_disposed = True

