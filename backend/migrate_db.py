#!/usr/bin/env python3
"""
Database migration script to add User table and user_id column to Task table
"""
import sqlite3
import sys
import os
from sqlmodel import SQLModel
# Add the parent directory to the path so we can import from the current directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models directly to get table definitions
from models import User, Task
from sqlmodel import create_engine

def migrate_database():
    # Connect to SQLite database directly
    db_path = os.path.join(os.path.dirname(__file__), '..', 'todo.db')
    sqlite_url = f"sqlite:///{db_path}"

    # Create engine for SQLite
    engine = create_engine(sqlite_url)

    # Create all tables defined in the models
    print("Creating all tables based on models...")
    SQLModel.metadata.create_all(engine)

    # Connect to SQLite database for manual operations
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if user_id column exists in task table (for existing databases)
        cursor.execute("PRAGMA table_info(task)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'user_id' not in columns:
            print("Adding user_id column to existing Task table...")
            # Add user_id column to existing task table
            cursor.execute('ALTER TABLE task ADD COLUMN user_id INTEGER DEFAULT 1')

        # Check if description column exists in task table
        if 'description' not in columns:
            print("Adding description column to existing Task table...")
            # Add description column to existing task table
            cursor.execute('ALTER TABLE task ADD COLUMN description TEXT')

        # Check if created_at column exists in task table
        if 'created_at' not in columns:
            print("Adding created_at column to existing Task table...")
            # Add created_at column to existing task table
            cursor.execute('ALTER TABLE task ADD COLUMN created_at TIMESTAMP')

        # Check if updated_at column exists in task table
        if 'updated_at' not in columns:
            print("Adding updated_at column to existing Task table...")
            # Add updated_at column to existing task table
            cursor.execute('ALTER TABLE task ADD COLUMN updated_at TIMESTAMP')

        # Commit transaction
        conn.commit()
        print("Database migration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()