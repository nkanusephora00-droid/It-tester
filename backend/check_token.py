#!/usr/bin/env python3
import requests

login_url = 'http://127.0.0.1:8000/auth/token'
me_url = 'http://127.0.0.1:8000/auth/me'

print('Login request...')
resp = requests.post(login_url, data={'username': 'admin', 'password': 'admin123'})
print('Login status:', resp.status_code)
print('Login body:', resp.text)
if resp.status_code == 200:
    token = resp.json().get('access_token')
    print('Token:', token[:20] + '...')
    print('Calling /auth/me...')
    resp2 = requests.get(me_url, headers={'Authorization': f'Bearer {token}'})
    print('Me status:', resp2.status_code)
    print('Me body:', resp2.text)
