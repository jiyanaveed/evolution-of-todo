#!/usr/bin/env python3
"""
Database migration script to add user authentication to existing database
"""
import sqlite3
import uuid
from datetime import datetime

def migrate_database():
    # Connect to the database
    conn = sqlite3.connect('../todo.db')
    cursor = conn.cursor()

    # Begin transaction
    cursor.execute('BEGIN TRANSACTION;')

    try:
        # Check if the user_id column exists in the task table
        cursor.execute("PRAGMA table_info(task);")
        columns = [column[1] for column in cursor.fetchall()]

        if 'user_id' not in columns:
            # Add user_id column to task table
            cursor.execute("ALTER TABLE task ADD COLUMN user_id TEXT NOT NULL DEFAULT 'default_user_id';")

        # Create user table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            );
        """)

        # Insert a default user if the user table is empty
        cursor.execute("SELECT COUNT(*) FROM user;")
        user_count = cursor.fetchone()[0]

        if user_count == 0:
            # Create a default user
            default_user_id = str(uuid.uuid4())
            default_email = "default@example.com"
            # Using a dummy password hash for the default user
            default_password_hash = "$2b$12$dummy_hash_for_default_user"

            cursor.execute("""
                INSERT INTO user (id, email, password_hash, created_at, is_active)
                VALUES (?, ?, ?, ?, ?);
            """, (default_user_id, default_email, default_password_hash, datetime.utcnow(), True))

            # Update all existing tasks to belong to the default user
            cursor.execute("UPDATE task SET user_id = ? WHERE user_id = ?;", (default_user_id, 'default_user_id'))

        # Commit the transaction
        conn.commit()
        print("Database migration completed successfully!")

    except Exception as e:
        # Rollback in case of error
        conn.rollback()
        print(f"Error during migration: {e}")
        raise

    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()