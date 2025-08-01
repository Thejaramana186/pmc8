#!/usr/bin/env python3
"""
Database Migration Script for PI Management System
This script adds the title column to existing user table
"""

import sqlite3
import os

def migrate_database():
    db_path = 'pi_management.db'
    
    if not os.path.exists(db_path):
        print("Database file not found. Creating new database...")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if title column exists
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'title' not in columns:
            print("Adding title column to user table...")
            cursor.execute("ALTER TABLE user ADD COLUMN title VARCHAR(10) DEFAULT 'Mr'")
            
            # Update existing users with default title
            cursor.execute("UPDATE user SET title = 'Mr' WHERE title IS NULL")
            
            conn.commit()
            print("✅ Title column added successfully!")
        else:
            print("✅ Title column already exists!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")

if __name__ == '__main__':
    migrate_database()