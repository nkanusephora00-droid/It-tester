#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from app.database import engine, SessionLocal
from app import models
from app.security import hash_password

print("=" * 60)
print("DATABASE CONNECTION TEST")
print("=" * 60)
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")

def test_connection():
    try:
        print("\n[1/5] Testing database connection...")
        with engine.connect() as conn:
            print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_tables():
    if not test_connection():
        return False
    print("\n[2/5] Checking database tables...")
    try:
        inspector = __import__('sqlalchemy').inspect(engine)
        tables = inspector.get_table_names()
        print(f"✅ Found {len(tables)} tables: {tables}")
        return True
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def check_users():
    print("\n[3/5] Checking users in database...")
    db = SessionLocal()
    try:
        users = db.query(models.User).all()
        print(f"✅ Found {len(users)} users:")
        for user in users:
            print(f"   - {user.username} ({user.email}) - Role: {user.role}")
        return len(users) > 0
    except Exception as e:
        print(f"❌ Error checking users: {e}")
        return False
    finally:
        db.close()

def check_settings():
    print("\n[4/5] Checking settings...")
    db = SessionLocal()
    try:
        settings = db.query(models.Setting).all()
        print(f"✅ Found {len(settings)} settings:")
        for s in settings:
            print(f"   - {s.key}: {s.value[:30]}..." if len(s.value) > 30 else f"   - {s.key}: {s.value}")
        return len(settings) > 0
    except Exception as e:
        print(f"❌ Error checking settings: {e}")
        return False
    finally:
        db.close()

def test_auth():
    print("\n[5/5] Testing authentication...")
    from app.security import verify_password
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.username == 'admin').first()
        if user:
            is_valid = verify_password('admin123', user.hashed_password)
            if is_valid:
                print("✅ Authentication test passed!")
                return True
            else:
                print("❌ Password verification failed!")
                return False
        else:
            print("⚠️ Admin user not found")
            return False
    except Exception as e:
        print(f"❌ Error testing auth: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print()
    success = True
    success &= test_connection()
    success &= check_tables()
    success &= check_users()
    success &= check_settings()
    success &= test_auth()

    print("\n" + "=" * 60)
    if success:
        print("✅ ALL CHECKS PASSED!")
    else:
        print("❌ SOME CHECKS FAILED!")
    print("=" * 60 + "\n")