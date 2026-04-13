#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app import models
from app.security import verify_password

def check_stored_hash():
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.username == 'admin').first()
        if user:
            print(f"Stored hash: {repr(user.hashed_password)}")
            print(f"Hash type: {type(user.hashed_password)}")
            print(f"Hash length: {len(user.hashed_password)}")

            # Test verification
            result = verify_password('admin123', user.hashed_password)
            print(f"Password verification result: {result}")

            # Test with wrong password
            wrong_result = verify_password('wrong', user.hashed_password)
            print(f"Wrong password verification result: {wrong_result}")
        else:
            print("User not found")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_stored_hash()