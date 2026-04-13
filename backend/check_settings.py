#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app import models

def check_settings():
    db = SessionLocal()
    try:
        settings = db.query(models.Setting).all()
        print(f"Found {len(settings)} settings")
        for s in settings:
            print(f"  {s.key}: {s.value[:20]}...")
    except Exception as e:
        print(f"Error checking settings: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_settings()