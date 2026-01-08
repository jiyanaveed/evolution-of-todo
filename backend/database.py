from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os
from dotenv import load_dotenv

# Load .env from the backend folder
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Check for Neon PostgreSQL first, then fall back to DATABASE_URL
NEON_URL = os.getenv("NEON_DATABASE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

if NEON_URL:
    # Use Neon PostgreSQL for production
    DATABASE_URL = NEON_URL
    print("Using Neon PostgreSQL database")
elif DATABASE_URL:
    print(f"Using DATABASE_URL: {DATABASE_URL}")
else:
    # Use SQLite as fallback if no DATABASE_URL is set
    # Use absolute path to ensure consistent database file location
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(project_root, "todo.db")
    DATABASE_URL = f"sqlite:///{db_path}"
    print(f"Using SQLite database: {db_path}")

# Create the SQLAlchemy engine
# For Neon PostgreSQL, ensure SSL is required
if DATABASE_URL.startswith("postgresql"):
    # Neon requires SSL, add pool settings for serverless
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
    )
else:
    # SQLite configuration
    engine = create_engine(DATABASE_URL, echo=False)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency function to get a database session for FastAPI.
    """
    with Session(engine) as session:
        yield session

def init_db():
    """
    Initialize the database by creating all tables.
    """
    try:
        # Try relative import first (for when running as module)
        from .models import User, Task, Conversation, Message  # Import models here to register them with SQLModel
    except ImportError:
        # Fallback to absolute import (for when running as script)
        from models import User, Task, Conversation, Message  # Import models here to register them with SQLModel
    SQLModel.metadata.create_all(engine)
