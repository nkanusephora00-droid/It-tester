#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from fastapi.testclient import TestClient
from app.main import app

def test_auth():
    client = TestClient(app)

    # Test login
    response = client.post(
        "/auth/token",
        data={"username": "admin", "password": "admin123"}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        data = response.json()
        print("✅ Login successful!")
        print(f"Access Token: {data.get('access_token', 'N/A')[:20]}...")
    else:
        print("❌ Login failed!")

if __name__ == "__main__":
    test_auth()