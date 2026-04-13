#!/usr/bin/env python3
import requests

# Test login
url = "http://localhost:8000/auth/token"
data = {
    "username": "admin",
    "password": "admin123"
}

print("Testing login with admin credentials...")
try:
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Login successful!")
        print(f"Access Token: {result.get('access_token', 'N/A')}")
        print(f"Token Type: {result.get('token_type', 'N/A')}")
    else:
        print("❌ Login failed!")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")