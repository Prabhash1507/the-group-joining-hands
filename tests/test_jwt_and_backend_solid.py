"""
===============================================================================
                        JOINING HANDS WEB ECOSYSTEM
            Enterprise Cryptographic JWT & Solid Backend Test Suite
                    File: tests/test_jwt_and_backend_solid.py
===============================================================================
"""

import unittest
import json
import urllib.request
import urllib.error
import time
import os

from app.helpers.jwt_auth import generate_jwt, verify_jwt, revoke_token, decode_jwt_unverified, is_token_blacklisted
from app.database.db import get_db, init_db

BASE_URL = 'http://localhost:8080'


class TestEnterpriseJWTAndBackend(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    # -------------------------------------------------------------------------
    # 1. PURE CRYPTOGRAPHIC JWT ENGINE UNIT TESTS
    # -------------------------------------------------------------------------
    def test_01_jwt_generation_and_claims(self):
        token = generate_jwt(user_id=1, email="test@joininghands.org", role="SUPER_ADMINISTRATOR", is_admin=True, full_name="Test Admin")
        self.assertIsInstance(token, str)
        self.assertEqual(token.count('.'), 2, "JWT must consist of exactly 3 dot-separated segments")

        is_valid, claims, err = verify_jwt(token)
        self.assertTrue(is_valid, f"Verification failed: {err}")
        self.assertIsNotNone(claims)
        self.assertEqual(claims.get('sub'), "1")
        self.assertEqual(claims.get('email'), "test@joininghands.org")
        self.assertEqual(claims.get('role'), "SUPER_ADMINISTRATOR")
        self.assertTrue(claims.get('is_admin'))
        self.assertEqual(claims.get('name'), "Test Admin")
        self.assertIn('iat', claims)
        self.assertIn('exp', claims)
        self.assertIn('jti', claims)

    def test_02_jwt_tampering_detection(self):
        token = generate_jwt(user_id=42, email="user@joininghands.org")
        parts = token.split('.')
        
        # Tamper with signature
        tampered_sig = parts[0] + '.' + parts[1] + '.TAMPERED_INVALID_SIGNATURE_123'
        is_valid, claims, err = verify_jwt(tampered_sig)
        self.assertFalse(is_valid)
        self.assertIn("signature", err.lower())

        # Tamper with payload
        fake_payload = '{"sub":"999","email":"hacker@evil.com"}'
        fake_payload_enc = parts[1][:-5] + 'AAAAA'
        tampered_payload = parts[0] + '.' + fake_payload_enc + '.' + parts[2]
        is_valid, claims, err = verify_jwt(tampered_payload)
        self.assertFalse(is_valid)

    def test_03_jwt_expiration(self):
        # Generate token with negative TTL (already expired)
        expired_token = generate_jwt(user_id=10, email="expired@joininghands.org", expires_in=-10)
        is_valid, claims, err = verify_jwt(expired_token)
        self.assertFalse(is_valid)
        self.assertIn("expired", err.lower())

    def test_04_jwt_revocation_blacklist(self):
        token = generate_jwt(user_id=5, email="revoked@joininghands.org")
        is_valid, claims, _ = verify_jwt(token)
        self.assertTrue(is_valid)

        # Revoke the token
        success = revoke_token(token, user_id=5, reason="Security test revocation")
        self.assertTrue(success)

        # Verification must now fail due to blacklist
        is_valid_after, _, err = verify_jwt(token)
        self.assertFalse(is_valid_after)
        self.assertIn("revoked", err.lower())

    # -------------------------------------------------------------------------
    # 2. LIVE HTTP API & BACKEND INTEGRATION TESTS
    # -------------------------------------------------------------------------
    def test_05_live_jwt_login_flow(self):
        login_url = f"{BASE_URL}/api/auth/login"
        payload = json.dumps({
            'email': 'member@joininghands.org',
            'password': 'demo1234'
        }).encode('utf-8')

        req = urllib.request.Request(login_url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get('success'))
            token = data.get('token')
            self.assertIsNotNone(token)
            self.assertEqual(token.count('.'), 2, "Returned auth token must be a signed 3-part JWT")

            # Verify client side decoding
            unverified = decode_jwt_unverified(token)
            self.assertIsNotNone(unverified)
            self.assertEqual(unverified.get('email'), 'member@joininghands.org')

    def test_06_protected_route_with_jwt_authorization(self):
        # 1. Login to get live JWT
        login_url = f"{BASE_URL}/api/auth/login"
        payload = json.dumps({'email': 'member@joininghands.org', 'password': 'demo1234'}).encode('utf-8')
        req = urllib.request.Request(login_url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            token = data['token']

        # 2. Access protected /api/auth/me
        me_url = f"{BASE_URL}/api/auth/me"
        me_req = urllib.request.Request(me_url, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        })
        with urllib.request.urlopen(me_req) as resp:
            self.assertEqual(resp.status, 200)
            me_data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(me_data.get('success'))
            self.assertEqual(me_data['user']['email'], 'member@joininghands.org')

    def test_07_token_verification_endpoint(self):
        # 1. Login to get live JWT
        login_url = f"{BASE_URL}/api/auth/login"
        payload = json.dumps({'email': 'member@joininghands.org', 'password': 'demo1234'}).encode('utf-8')
        req = urllib.request.Request(login_url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            token = data['token']

        # 2. Post to /api/auth/verify-token
        verify_url = f"{BASE_URL}/api/auth/verify-token"
        verify_payload = json.dumps({'token': token}).encode('utf-8')
        verify_req = urllib.request.Request(verify_url, data=verify_payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(verify_req) as resp:
            self.assertEqual(resp.status, 200)
            v_data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(v_data.get('success'))
            self.assertTrue(v_data.get('valid'))
            self.assertEqual(v_data['claims']['email'], 'member@joininghands.org')

    def test_08_logout_and_jwt_revocation_enforcement(self):
        # 1. Login to get distinct JWT
        login_url = f"{BASE_URL}/api/auth/login"
        payload = json.dumps({'email': 'member@joininghands.org', 'password': 'demo1234'}).encode('utf-8')
        req = urllib.request.Request(login_url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            token = data['token']

        # 2. Logout via /api/auth/logout
        logout_url = f"{BASE_URL}/api/auth/logout"
        logout_req = urllib.request.Request(logout_url, data=b'{}', headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        })
        with urllib.request.urlopen(logout_req) as resp:
            self.assertEqual(resp.status, 200)
            l_data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(l_data.get('success'))

        # 3. Subsequent request with revoked token must return 401 Unauthorized
        me_url = f"{BASE_URL}/api/auth/me"
        me_req = urllib.request.Request(me_url, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        })
        try:
            urllib.request.urlopen(me_req)
            self.fail("Expected HTTPError 401 for revoked JWT token")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 401)

    def test_09_security_headers_inspection(self):
        req = urllib.request.Request(f"{BASE_URL}/")
        with urllib.request.urlopen(req) as resp:
            headers = dict(resp.headers)
            self.assertEqual(headers.get('X-Content-Type-Options'), 'nosniff')
            self.assertEqual(headers.get('X-Frame-Options'), 'SAMEORIGIN')
            self.assertEqual(headers.get('Referrer-Policy'), 'strict-origin-when-cross-origin')
            self.assertIn('Content-Security-Policy', headers)


if __name__ == '__main__':
    unittest.main()
