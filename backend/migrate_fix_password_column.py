"""
Final Database Migration: Rename password_hash to hashed_password
This aligns the database schema with the application model
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def fix_password_column():
    """Rename password_hash to hashed_password"""

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("[ERROR] DATABASE_URL not found in .env file")
        return False

    try:
        print("[1/4] Connecting to database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        # Check current columns
        print("[2/4] Checking current schema...")
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='user'
            ORDER BY ordinal_position;
        """)
        columns = [row[0] for row in cursor.fetchall()]
        print(f"      Current columns: {columns}")

        # Drop the empty hashed_password column if it exists
        if 'hashed_password' in columns:
            print("[3/4] Dropping empty hashed_password column...")
            cursor.execute('ALTER TABLE "user" DROP COLUMN hashed_password;')
            conn.commit()

        # Rename password_hash to hashed_password
        if 'password_hash' in columns:
            print("[4/4] Renaming password_hash to hashed_password...")
            cursor.execute('ALTER TABLE "user" RENAME COLUMN password_hash TO hashed_password;')
            conn.commit()

        # Verify final schema
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='user'
            ORDER BY ordinal_position;
        """)
        final_columns = [row[0] for row in cursor.fetchall()]
        print(f"\n      Final columns: {final_columns}")

        print("\n[SUCCESS] Database schema fixed!")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"\n[ERROR] Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Final Migration: Fix password column naming")
    print("=" * 60)
    print()

    success = fix_password_column()

    print()
    if success:
        print("=" * 60)
        print("[SUCCESS] Database is ready!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Restart backend server (Ctrl+C then restart)")
        print("2. Test registration at http://localhost:3000")
    else:
        print("=" * 60)
        print("[FAILED] Migration did not complete")
        print("=" * 60)
