#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app import models
from app.security import hash_password
import secrets

def setup_secret_key():
    print("Setting up secret key...")
    db = SessionLocal()
    try:
        # Check if SECRET_KEY already exists
        existing = db.query(models.Setting).filter(models.Setting.key == "SECRET_KEY").first()
        if existing:
            print("✅ SECRET_KEY already exists")
            return True

        # Create SECRET_KEY
        secret_key = secrets.token_hex(32)
        setting = models.Setting(key="SECRET_KEY", value=secret_key)
        db.add(setting)
        db.commit()
        print("✅ SECRET_KEY created successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def reset_admin_password():
    print("\nResetting admin password...")
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.username == "admin").first()
        if user:
            new_hash = hash_password("admin123")
            user.hashed_password = new_hash
            db.commit()
            print("✅ Admin password reset to: admin123")
            return True
        else:
            print("❌ Admin user not found")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    setup_secret_key()
    reset_admin_password()
    print("\n✅ Database setup complete!")