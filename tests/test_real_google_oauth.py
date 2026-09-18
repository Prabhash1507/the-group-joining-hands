"""
===============================================================================
                        JOINING HANDS WEB ECOSYSTEM
                     Real Google OAuth 2.0 Integration Test Suite
                     File: tests/test_real_google_oauth.py
===============================================================================
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import json
import io

# Add parent directory to path so we can import the server
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock environment variables before importing server (fallbacks to dummy values if not in environment)
os.environ['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID', 'dummy-google-client-id-for-tests')
os.environ['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET', 'dummy-google-client-secret-for-tests')
os.environ['APP_ENV'] = 'production'

from server import EnterpriseRESTRequestHandler
from app.database.db import get_db, init_db

class MockSocket:
    def __init__(self, rfile_content=b""):
        self.rfile = io.BytesIO(rfile_content)
        self.wfile = io.BytesIO()

class TestableHandler(EnterpriseRESTRequestHandler):
    def __init__(self, mock_socket, headers=None):
        self.connection = mock_socket
        self.rfile = mock_socket.rfile
        self.wfile = mock_socket.wfile
        self.client_address = ('127.0.0.1', 12345)
        self.headers = headers or {}
        
    def send_response(self, code, message=None):
        self.wfile.write(f"HTTP/1.1 {code} OK\r\n".encode('utf-8'))
        
    def send_header(self, keyword, value):
        self.wfile.write(f"{keyword}: {value}\r\n".encode('utf-8'))
        
    def end_headers(self):
        self.wfile.write(b"\r\n")

class TestRealGoogleOAuth(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        init_db()

    def setUp(self):
        # Clean up database test entries before each test
        conn = get_db()
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = OFF")
            cursor.execute("DELETE FROM users WHERE email IN ('oauth_new_user@gmail.com', 'oauth_existing@gmail.com')")
            conn.commit()
        finally:
            conn.close()

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_oauth_signup_new_user(self, mock_verify):
        """Test that a new Google user successfully signs up and creates a DB row."""
        # 1. Mock Google OIDC token verification return payload
        mock_verify.return_value = {
            'iss': 'https://accounts.google.com',
            'sub': 'google_sub_unique_123',
            'email': 'oauth_new_user@gmail.com',
            'email_verified': True,
            'name': 'Google OAuth Tester',
            'picture': 'https://google.com/avatar.png'
        }

        # 2. Build mock request to POST /api/auth/google
        post_data = json.dumps({'credential': 'valid-google-id-token'}).encode('utf-8')
        mock_socket = MockSocket(post_data)
        
        # Instantiate testable request handler
        handler = TestableHandler(
            mock_socket,
            headers={
                'Content-Length': str(len(post_data)),
                'Origin': 'http://localhost:8080'
            }
        )
        handler.path = '/api/auth/google'
        
        # Execute post routing logic
        handler.do_POST()
        
        # Inspect response written to wfile
        response_bytes = mock_socket.wfile.getvalue()
        response_str = response_bytes.decode('utf-8')
        json_start = response_str.find('{')
        response_json = json.loads(response_str[json_start:])
        
        # Asserts
        self.assertTrue(response_json.get('success'), f"Response failed: {response_json}")
        self.assertEqual(response_json.get('authMode'), 'GOOGLE_OIDC')
        self.assertIsNotNone(response_json.get('token'))
        
        # Check DB row creation
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, google_id, full_name, avatar_url FROM users WHERE email = 'oauth_new_user@gmail.com'")
        row = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(row)
        self.assertEqual(row[1], 'oauth_new_user@gmail.com')
        self.assertEqual(row[2], 'google_sub_unique_123')
        self.assertEqual(row[3], 'Google OAuth Tester')
        self.assertEqual(row[4], 'https://google.com/avatar.png')

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_oauth_link_existing_user(self, mock_verify):
        """Test that Google login links to an existing email account rather than duplicating it."""
        # 1. Create an existing user with email/password but no google_id
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, full_name, password_hash, google_id) VALUES (?, ?, ?, NULL)",
            ('oauth_existing@gmail.com', 'Existing Member', 'some_password_hash')
        )
        conn.commit()
        conn.close()

        # 2. Mock Google OIDC token verification return payload
        mock_verify.return_value = {
            'iss': 'https://accounts.google.com',
            'sub': 'google_sub_linked_456',
            'email': 'oauth_existing@gmail.com',
            'email_verified': True,
            'name': 'Existing Member',
            'picture': 'https://google.com/new_avatar.png'
        }

        # 3. Build mock request to POST /api/auth/google
        post_data = json.dumps({'credential': 'valid-google-id-token'}).encode('utf-8')
        mock_socket = MockSocket(post_data)
        
        handler = TestableHandler(
            mock_socket,
            headers={
                'Content-Length': str(len(post_data)),
                'Origin': 'http://localhost:8080'
            }
        )
        handler.path = '/api/auth/google'
        
        # Execute post routing logic
        handler.do_POST()
        
        # Inspect response
        response_bytes = mock_socket.wfile.getvalue()
        response_str = response_bytes.decode('utf-8')
        json_start = response_str.find('{')
        response_json = json.loads(response_str[json_start:])
        
        self.assertTrue(response_json.get('success'))
        
        # Check DB row was updated/linked (not duplicated)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, google_id FROM users WHERE email = 'oauth_existing@gmail.com'")
        rows = cursor.fetchall()
        conn.close()
        
        self.assertEqual(len(rows), 1, "Should not create duplicate email rows")
        self.assertEqual(rows[0][2], 'google_sub_linked_456', "google_id must be linked")

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_oauth_unverified_email_rejection(self, mock_verify):
        """Test that unverified Google accounts are rejected."""
        mock_verify.return_value = {
            'iss': 'https://accounts.google.com',
            'sub': 'google_sub_unverified',
            'email': 'unverified@gmail.com',
            'email_verified': False,
            'name': 'Unverified Tester'
        }

        post_data = json.dumps({'credential': 'unverified-email-token'}).encode('utf-8')
        mock_socket = MockSocket(post_data)
        
        handler = TestableHandler(
            mock_socket,
            headers={
                'Content-Length': str(len(post_data)),
                'Origin': 'http://localhost:8080'
            }
        )
        handler.path = '/api/auth/google'
        
        handler.do_POST()
        
        response_bytes = mock_socket.wfile.getvalue()
        response_str = response_bytes.decode('utf-8')
        json_start = response_str.find('{')
        response_json = json.loads(response_str[json_start:])
        
        self.assertFalse(response_json.get('success'))
        self.assertIn('not verified', response_json.get('error', '').lower())

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_oauth_invalid_issuer_rejection(self, mock_verify):
        """Test that non-Google issuers are rejected."""
        mock_verify.return_value = {
            'iss': 'evil_issuer.com',
            'sub': 'google_sub_evil',
            'email': 'evil@gmail.com',
            'email_verified': True,
            'name': 'Evil Tester'
        }

        post_data = json.dumps({'credential': 'evil-issuer-token'}).encode('utf-8')
        mock_socket = MockSocket(post_data)
        
        handler = TestableHandler(
            mock_socket,
            headers={
                'Content-Length': str(len(post_data)),
                'Origin': 'http://localhost:8080'
            }
        )
        handler.path = '/api/auth/google'
        
        handler.do_POST()
        
        response_bytes = mock_socket.wfile.getvalue()
        response_str = response_bytes.decode('utf-8')
        json_start = response_str.find('{')
        response_json = json.loads(response_str[json_start:])
        
        self.assertFalse(response_json.get('success'))
        self.assertIn('invalid issuer', response_json.get('error', '').lower())

    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_oauth_expired_token_rejection(self, mock_verify):
        """Test that expired or signature-mismatched tokens are rejected."""
        mock_verify.side_effect = ValueError("Token expired")

        post_data = json.dumps({'credential': 'expired-token'}).encode('utf-8')
        mock_socket = MockSocket(post_data)
        
        handler = TestableHandler(
            mock_socket,
            headers={
                'Content-Length': str(len(post_data)),
                'Origin': 'http://localhost:8080'
            }
        )
        handler.path = '/api/auth/google'
        
        handler.do_POST()
        
        response_bytes = mock_socket.wfile.getvalue()
        response_str = response_bytes.decode('utf-8')
        json_start = response_str.find('{')
        response_json = json.loads(response_str[json_start:])
        
        self.assertFalse(response_json.get('success'))
        self.assertIn('verification failed', response_json.get('error', '').lower())
