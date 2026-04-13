#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from app.database import engine, SessionLocal
from app import models
from app.security import hash_password

print("DATABASE_URL:", os.environ.get('DATABASE_URL'))

def test_connection():
    try:
        with engine.connect() as conn:
            print("Database connection successful")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

def create_tables():
    if not test_connection():
        return False
    print("Creating database tables...")
    try:
        models.Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

def create_admin_user():
    if not test_connection():
        return False
    print("Creating admin user...")
    db = SessionLocal()
    try:
        # Check if admin user already exists
        existing_user = db.query(models.User).filter(models.User.username == "admin").first()
        if existing_user:
            print("Admin user already exists")
            return True

        # Create admin user
        hashed_password = hash_password("admin123")
        user = models.User(
            username="admin",
            email="admin@example.com",
            hashed_password=hashed_password,
            role="admin",
            is_active=True
        )
        db.add(user)
        db.commit()
        print("Admin user created successfully")
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def create_secret_key():
    if not test_connection():
        return False
    print("Creating secret key...")
    db = SessionLocal()
    try:
        # Check if SECRET_KEY already exists
        existing_setting = db.query(models.Setting).filter(models.Setting.key == "SECRET_KEY").first()
        if existing_setting:
            print("SECRET_KEY already exists")
            return True

        # Create SECRET_KEY
        import secrets
        secret_key = secrets.token_hex(32)
        setting = models.Setting(key="SECRET_KEY", value=secret_key)
        db.add(setting)
        db.commit()
        print("SECRET_KEY created successfully")
        return True
    except Exception as e:
        print(f"Error creating secret key: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def list_users():
    if not test_connection():
        return False
    print("Listing users...")
    db = SessionLocal()
    try:
        users = db.query(models.User).all()
        print(f"Found {len(users)} users:")
        for user in users:
            print(f"  - {user.username} ({user.email}) - Active: {user.is_active} - Role: {user.role}")
        return True
    except Exception as e:
        print(f"Error listing users: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = True
    success &= create_tables()
    if success:
        success &= create_secret_key()
    if success:
        success &= create_admin_user()
    if success:
        success &= list_users()

    if success:
        print("\n✅ Database setup completed successfully!")
    else:
        print("\n❌ Database setup failed!")