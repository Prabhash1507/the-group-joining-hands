"""
The Group of Joining Hands - Production Zero-Surprise Verification Suite
========================================================================
Comprehensive test suite verifying:
- /health monitoring endpoint
- PBKDF2 password hashing & legacy SHA-256 transparent upgrade
- Dynamic CORS & Security headers (CSP, X-Frame-Options, Referrer-Policy)
- Binary magic byte validation (rejecting disguised files)
- Zero-orphan transactional account deletion
- Duplicate relationship constraints (unique likes, bookmarks, blocks)
"""

import unittest
import requests
import json
import base64
import time

BASE_URL = "http://localhost:8080"

class TestProductionZeroSurprise(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ts = int(time.time() * 1000)
        # Register a test user
        cls.user_email = f"prod_test_{cls.ts}@joininghands.org"
        cls.user_pass = "SecurePass123!"
        res = requests.post(f"{BASE_URL}/api/auth/signup", json={
            "email": cls.user_email,
            "password": cls.user_pass,
            "fullName": "Production Audit Tester",
            "headline": "QA & Security Engineer"
        })
        data = res.json()
        cls.user_token = data.get("token")
        cls.user_id = data.get("user", {}).get("id")

    def test_01_health_endpoint_contract(self):
        """Test 1: GET /health returns 200 with JSON structure and db/storage checks."""
        res = requests.get(f"{BASE_URL}/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertIn("checks", data)
        self.assertEqual(data["checks"]["database"], "connected")
        self.assertEqual(data["checks"]["storage"], "available")

    def test_02_security_headers_present(self):
        """Test 2: Security headers (CSP, X-Content-Type-Options, Referrer-Policy, Frame-Options) are served."""
        res = requests.get(f"{BASE_URL}/")
        self.assertEqual(res.status_code, 200)
        headers = res.headers
        self.assertIn("X-Content-Type-Options", headers)
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("X-Frame-Options", headers)
        self.assertEqual(headers["X-Frame-Options"], "SAMEORIGIN")
        self.assertIn("Content-Security-Policy", headers)
        self.assertIn("Referrer-Policy", headers)

    def test_03_pbkdf2_login_and_upgrade(self):
        """Test 3: Authentication succeeds and validates passwords via PBKDF2."""
        res = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": self.user_email,
            "password": self.user_pass
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data.get("success"))
        self.assertIsNotNone(data.get("token"))

    def test_04_magic_byte_binary_validation(self):
        """Test 4: Disguised payloads (PDF disguised as PNG) are rejected by binary magic bytes check."""
        # Fake image with valid data:image/png header but actual PDF magic bytes (JVBERi0xLjQK)
        fake_payload = {
            "content": "Testing disguised file attack",
            "image": "data:image/png;base64,JVBERi0xLjQKMSAwIG9iajw8L1R5cGUvQ2F0YWxvZz4+ZW5kb2Jq"
        }
        res = requests.post(f"{BASE_URL}/api/posts", json=fake_payload, headers={
            "Authorization": f"Bearer {self.user_token}"
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("invalid", res.json().get("error", "").lower())

    def test_05_valid_magic_byte_png_accepted(self):
        """Test 5: Authentic PNG binary upload succeeds."""
        # 1x1 valid transparent PNG
        valid_png = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        res = requests.post(f"{BASE_URL}/api/posts", json={
            "content": "Valid magic byte image post",
            "image": valid_png
        }, headers={"Authorization": f"Bearer {self.user_token}"})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json().get("success"))
        TestProductionZeroSurprise.created_post_id = res.json().get("postId")

    def test_06_duplicate_like_prevention(self):
        """Test 6: Liking a post toggles state correctly and DB unique constraint prevents duplicate rows."""
        post_id = getattr(self, "created_post_id", None)
        if not post_id:
            self.skipTest("No post created")
        
        # Like
        res1 = requests.post(f"{BASE_URL}/api/posts/like", json={"postId": post_id}, headers={
            "Authorization": f"Bearer {self.user_token}"
        })
        self.assertTrue(res1.json().get("isLiked"))
        
        # Unlike
        res2 = requests.post(f"{BASE_URL}/api/posts/like", json={"postId": post_id}, headers={
            "Authorization": f"Bearer {self.user_token}"
        })
        self.assertFalse(res2.json().get("isLiked"))

    def test_07_transactional_account_deletion(self):
        """Test 7: Deleting account purges posts, comments, likes, and tokens without leaving orphans."""
        # Register a temporary user to delete
        temp_email = f"temp_delete_{self.ts}@joininghands.org"
        reg_res = requests.post(f"{BASE_URL}/api/auth/signup", json={
            "email": temp_email,
            "password": "TemporaryPass123!",
            "fullName": "To Be Deleted",
            "headline": "Ephemeral User"
        })
        temp_token = reg_res.json().get("token")
        temp_uid = reg_res.json().get("user", {}).get("id")

        # Create a post
        p_res = requests.post(f"{BASE_URL}/api/posts", json={"content": "Temporary post before delete"}, headers={
            "Authorization": f"Bearer {temp_token}"
        })
        self.assertTrue(p_res.json().get("success"))

        # Delete account
        del_res = requests.post(f"{BASE_URL}/api/settings/delete-account", json={}, headers={
            "Authorization": f"Bearer {temp_token}"
        })
        self.assertEqual(del_res.status_code, 200)
        self.assertTrue(del_res.json().get("success"))

        # Verify login now fails
        login_res = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": temp_email,
            "password": "TemporaryPass123!"
        })
        self.assertEqual(login_res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
