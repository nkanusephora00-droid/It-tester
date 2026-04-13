#!/usr/bin/env python3
import requests

# Login first
login_resp = requests.post('http://127.0.0.1:8000/auth/token', data={'username': 'admin', 'password': 'admin123'})
print('Login status:', login_resp.status_code)

if login_resp.status_code == 200:
    token = login_resp.json()['access_token']
    print('Token obtained successfully')

    # Test /auth/me
    me_resp = requests.get('http://127.0.0.1:8000/auth/me', headers={'Authorization': f'Bearer {token}'})
    print('ME status:', me_resp.status_code)
    print('ME body:', me_resp.text)

    if me_resp.status_code != 200:
        print('ERROR: /auth/me failed!')
    else:
        print('SUCCESS: /auth/me works!')
else:
    print('ERROR: Login failed!')
    print('Login body:', login_resp.text)