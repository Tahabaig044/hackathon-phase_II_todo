"""
Database Migration: Add name column to user table
Run this script to fix the missing 'name' column error
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def migrate():
    """Add name column to user table"""

    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("[ERROR] DATABASE_URL not found in .env file")
        return False

    try:
        # Connect to database
        print("[1/3] Connecting to database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        # Check if name column exists
        print("[2/3] Checking if 'name' column exists...")
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='user' AND column_name='name';
        """)

        if cursor.fetchone():
            print("[OK] Column 'name' already exists. No migration needed.")
            cursor.close()
            conn.close()
            return True

        # Add name column
        print("[3/3] Adding 'name' column to user table...")
        cursor.execute("""
            ALTER TABLE "user"
            ADD COLUMN name VARCHAR NOT NULL DEFAULT 'User';
        """)

        conn.commit()
        print("[SUCCESS] Migration completed successfully!")
        print("          Column 'name' added to user table")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"[ERROR] Migration failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Database Migration: Add name column to user table")
    print("=" * 60)
    print()

    success = migrate()

    print()
    if success:
        print("=" * 60)
        print("[SUCCESS] Database is now ready!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Restart your backend server")
        print("2. Try registering again at http://localhost:3000")
    else:
        print("=" * 60)
        print("[FAILED] Migration did not complete")
        print("=" * 60)
        print()
        print("Please check the error message above")
