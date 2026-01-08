#!/usr/bin/env python3
"""
Simple test script to check database connectivity and model definitions
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from database import init_db, engine
from models import User, Task, Conversation, Message
from sqlmodel import select, Session

def test_db():
    print("Testing database connection and models...")

    try:
        # Initialize database
        print("Initializing database...")
        init_db()
        print("Database initialized successfully!")

        # Test session
        print("Testing database session...")
        with Session(engine) as session:
            # Try to query users (should be empty initially)
            users = session.exec(select(User)).all()
            print(f"Found {len(users)} users in database")

        print("Database test completed successfully!")

    except Exception as e:
        print(f"Database test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_db()