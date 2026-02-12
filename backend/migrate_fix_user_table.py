"""
Comprehensive Database Migration: Fix user table schema
Checks and adds all missing columns to match the application model
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def check_and_migrate():
    """Check current schema and add missing columns"""

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("[ERROR] DATABASE_URL not found in .env file")
        return False

    try:
        print("[1/5] Connecting to database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        # Check current columns
        print("[2/5] Checking current user table schema...")
        cursor.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name='user'
            ORDER BY ordinal_position;
        """)

        existing_columns = {row[0]: row[1] for row in cursor.fetchall()}
        print(f"      Found columns: {list(existing_columns.keys())}")

        # Define required columns
        required_columns = {
            'id': 'uuid',
            'name': 'character varying',
            'email': 'character varying',
            'hashed_password': 'character varying',
            'created_at': 'timestamp without time zone',
            'updated_at': 'timestamp without time zone'
        }

        missing_columns = []
        for col_name, col_type in required_columns.items():
            if col_name not in existing_columns:
                missing_columns.append(col_name)

        if not missing_columns:
            print("[OK] All required columns exist. No migration needed.")
            cursor.close()
            conn.close()
            return True

        print(f"[3/5] Missing columns detected: {missing_columns}")

        # Add missing columns
        print("[4/5] Adding missing columns...")

        migrations = []
        if 'name' in missing_columns:
            migrations.append("ALTER TABLE \"user\" ADD COLUMN name VARCHAR NOT NULL DEFAULT 'User';")

        if 'hashed_password' in missing_columns:
            migrations.append("ALTER TABLE \"user\" ADD COLUMN hashed_password VARCHAR NOT NULL DEFAULT '';")

        if 'created_at' in missing_columns:
            migrations.append("ALTER TABLE \"user\" ADD COLUMN created_at TIMESTAMP NOT NULL DEFAULT NOW();")

        if 'updated_at' in missing_columns:
            migrations.append("ALTER TABLE \"user\" ADD COLUMN updated_at TIMESTAMP;")

        for i, migration in enumerate(migrations, 1):
            print(f"      [{i}/{len(migrations)}] {migration}")
            cursor.execute(migration)

        conn.commit()

        print("[5/5] Verifying schema...")
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='user'
            ORDER BY ordinal_position;
        """)
        final_columns = [row[0] for row in cursor.fetchall()]
        print(f"      Final columns: {final_columns}")

        print("[SUCCESS] Migration completed successfully!")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"[ERROR] Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Comprehensive Database Migration: Fix user table")
    print("=" * 60)
    print()

    success = check_and_migrate()

    print()
    if success:
        print("=" * 60)
        print("[SUCCESS] Database schema is now correct!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Restart your backend server (Ctrl+C then restart)")
        print("2. Try registering at http://localhost:3000")
    else:
        print("=" * 60)
        print("[FAILED] Migration did not complete")
        print("=" * 60)
