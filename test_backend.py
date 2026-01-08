#!/usr/bin/env python3
"""
Test script to debug backend module imports and functionality
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing backend imports...")

try:
    print("Importing models...")
    from backend.models import User, Task, UserCreate
    print("✓ Models imported successfully")

    print("Importing database...")
    from backend.database import init_db, get_session
    print("✓ Database imported successfully")

    print("Importing CRUD...")
    from backend import crud
    print("✓ CRUD imported successfully")

    print("Importing auth...")
    from backend import auth
    print("✓ Auth imported successfully")

    print("Testing database initialization...")
    init_db()
    print("✓ Database initialized successfully")

    print("Testing session creation...")
    session_gen = get_session()
    session = next(session_gen)
    print("✓ Session created successfully")

    print("Testing user retrieval...")
    existing_user = crud.get_user_by_email(session, "test@example.com")
    if existing_user:
        print(f"✓ User already exists: {existing_user.email}")
        test_user = existing_user
    else:
        print("Testing user creation...")
        test_user = crud.create_user(session, "test@example.com", "testpassword")
        print(f"✓ User created: {test_user.email}")

    print("Testing user retrieval...")
    retrieved_user = crud.get_user_by_email(session, "test@example.com")
    print(f"✓ User retrieved: {retrieved_user.email if retrieved_user else 'None'}")

    print("All tests passed!")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()