#!/usr/bin/env python3
import requests

url = "http://127.0.0.1:8000/auth/token"
print(f"Requesting {url}")
try:
    response = requests.post(url, data={"username": "admin", "password": "admin123"})
    print("Status code:", response.status_code)
    print("Response text:", response.text)
except Exception as e:
    print("Request error:", e)
