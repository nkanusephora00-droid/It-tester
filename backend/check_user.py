#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app import models

def check_user():
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.username == 'admin').first()
        if user:
            print(f"✅ User found: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Active: {user.is_active}")
            print(f"   Role: {user.role}")
            print(f"   Password hash length: {len(user.hashed_password)}")
        else:
            print("❌ User not found")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_user()