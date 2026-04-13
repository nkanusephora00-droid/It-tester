#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.security import verify_password, hash_password

def test_password_functions():
    pwd = 'admin123'
    print(f"Testing password: {pwd}")

    # Hash the password
    hashed = hash_password(pwd)
    print(f"Hashed password: {hashed}")
    print(f"Hash type: {type(hashed)}")
    print(f"Hash length: {len(hashed)}")

    # Verify the password
    is_valid = verify_password(pwd, hashed)
    print(f"Password verification: {is_valid}")

    # Test with wrong password
    wrong_pwd = 'wrong123'
    is_invalid = verify_password(wrong_pwd, hashed)
    print(f"Wrong password verification: {is_invalid}")

if __name__ == "__main__":
    test_password_functions()