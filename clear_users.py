#!/usr/bin/env python3
"""
Script to clear all users from the database
"""
import sqlite3
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), 'todo.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Current users in the database:")
cursor.execute("SELECT id, email FROM user")
users = cursor.fetchall()
for user in users:
    print(f"  ID: {user[0]}, Email: {user[1]}")

print(f"\nTotal users before deletion: {len(users)}")

# Delete all users
cursor.execute("DELETE FROM user")

# Since tasks are linked to users, let's also clear tasks to avoid foreign key issues
cursor.execute("DELETE FROM task")

# Commit the changes
conn.commit()

print("All users and tasks have been deleted from the database.")

# Verify deletion
cursor.execute("SELECT COUNT(*) FROM user")
count = cursor.fetchone()[0]
print(f"Total users after deletion: {count}")

conn.close()
print("Database connection closed.")