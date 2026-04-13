#!/usr/bin/env python3
import requests

# Test the full auth flow
def test_auth_flow():
    print("=== Testing Auth Flow ===")

    # 1. Login
    print("\n1. Login request...")
    login_resp = requests.post(
        'http://127.0.0.1:8000/auth/token',
        data={'username': 'admin', 'password': 'admin123'}
    )
    print(f"Login status: {login_resp.status_code}")

    if login_resp.status_code != 200:
        print(f"Login failed: {login_resp.text}")
        return

    token = login_resp.json()['access_token']
    print(f"Token received: {token[:20]}...")

    # 2. Test /auth/me
    print("\n2. Testing /auth/me...")
    me_resp = requests.get(
        'http://127.0.0.1:8000/auth/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    print(f"Me status: {me_resp.status_code}")
    print(f"Me response: {me_resp.text}")

    if me_resp.status_code == 200:
        print("✅ Auth flow works!")
    else:
        print("❌ Auth flow broken!")

if __name__ == "__main__":
    test_auth_flow()