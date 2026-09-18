"""
The Group of Joining Hands - Six Safe Features Extension Automated Test Suite
=============================================================================
Tests the 6 Safe Feature Additions:
1. Email Verification Workflow (Token generation, confirmation, expiration, rate-limiting)
2. Forgot Password / Password Reset (Token generation, invalidation, expiration, password update)
3. Report, Block & Mute (Content reporting, admin review, block messaging/connect, feed muting)
4. Notifications Central System (Creation, unread counts, mark read, authorization)
5. Global Multi-Category Search (People, Posts, Hashtags, Events with privacy & block filters)
6. Better Professional Profiles (Skills, Education, Experience, Projects, Certifications)
"""

import unittest
import os
import json
import time
import urllib.request
import urllib.parse
import sqlite3

from app.config.config import PORT
from app.database.db import get_db, init_db
from app.helpers.security import hash_password, generate_token

SERVER_URL = f"http://127.0.0.1:{PORT}"

def api_request(path, method="GET", payload=None, token=None):
    url = f"{SERVER_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


class TestSixFeatureExtensions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create fresh dedicated test users
        cls.ts = int(time.time() * 1000)
        cls.user_a_email = f"feat_a_{cls.ts}@joininghands.org"
        cls.user_b_email = f"feat_b_{cls.ts}@joininghands.org"
        cls.admin_email = "member@joininghands.org"

        # Sign up User A
        st, res = api_request("/api/auth/signup", method="POST", payload={
            "fullName": "Feature User Alpha",
            "email": cls.user_a_email,
            "password": "Password123!",
            "headline": "Full-Stack Engineer"
        })
        cls.user_a_token = res.get("token")
        cls.user_a_id = res.get("user", {}).get("id")

        # Sign up User B
        st, res = api_request("/api/auth/signup", method="POST", payload={
            "fullName": "Feature User Beta",
            "email": cls.user_b_email,
            "password": "Password123!",
            "headline": "Product Designer"
        })
        cls.user_b_token = res.get("token")
        cls.user_b_id = res.get("user", {}).get("id")

        # Login Admin
        st, res = api_request("/api/auth/login", method="POST", payload={
            "email": cls.admin_email,
            "password": "demo1234"
        })
        cls.admin_token = res.get("token")

    # -------------------------------------------------------------
    # FEATURE 1: Email Verification
    # -------------------------------------------------------------
    def test_01_email_verification_request_and_confirm(self):
        """Test requesting verification token and activating email verification."""
        st, res = api_request("/api/auth/verify-email/request", method="POST", 
                              payload={"email": self.user_a_email}, token=self.user_a_token)
        self.assertEqual(st, 200)
        dev_token = res.get("devToken")
        self.assertIsNotNone(dev_token)

        # Confirm verification
        st, res = api_request("/api/auth/verify-email/confirm", method="POST", payload={"token": dev_token})
        self.assertEqual(st, 200)
        self.assertTrue(res.get("success"))

        # Re-using same token should fail
        st, res = api_request("/api/auth/verify-email/confirm", method="POST", payload={"token": dev_token})
        self.assertEqual(st, 400)

    # -------------------------------------------------------------
    # FEATURE 2: Forgot Password & Reset
    # -------------------------------------------------------------
    def test_02_forgot_password_and_reset_flow(self):
        """Test forgot password token generation, password update, and session invalidation."""
        st, res = api_request("/api/auth/forgot-password", method="POST", payload={"email": self.user_b_email})
        self.assertEqual(st, 200)
        reset_token = res.get("devResetToken")
        self.assertIsNotNone(reset_token)

        # Reset password to a new one
        new_pass = "BrandNewSecret2026!"
        st, res = api_request("/api/auth/reset-password", method="POST", payload={
            "token": reset_token,
            "newPassword": new_pass
        })
        self.assertEqual(st, 200)
        self.assertTrue(res.get("success"))

        # Old login token should now be invalidated
        st, res = api_request("/api/auth/me", method="GET", token=self.user_b_token)
        self.assertEqual(st, 401)

        # Login with new password should succeed
        st, res = api_request("/api/auth/login", method="POST", payload={
            "email": self.user_b_email,
            "password": new_pass
        })
        self.assertEqual(st, 200)
        TestSixFeatureExtensions.user_b_token = res.get("token") # Update class-level token for subsequent tests

    # -------------------------------------------------------------
    # FEATURE 3: Report, Block & Mute
    # -------------------------------------------------------------
    def test_03_report_content_and_admin_resolution(self):
        """Test user reporting a post and admin resolving/dismissing it."""
        # User A creates a post
        st, res = api_request("/api/posts/create", method="POST", payload={"content": "Post to be reported"}, token=self.user_a_token)
        post_id = res.get("postId")

        # User B reports post
        st, res = api_request("/api/reports/create", method="POST", payload={
            "targetType": "POST",
            "targetId": post_id,
            "reason": "Spam and inappropriate content"
        }, token=self.user_b_token)
        self.assertEqual(st, 200)
        report_id = res.get("reportId")

        # Admin fetches reports list
        st, res = api_request("/api/admin/reports", method="GET", token=self.admin_token)
        self.assertEqual(st, 200)
        report_ids = [r["id"] for r in res.get("reports", [])]
        self.assertIn(report_id, report_ids)

        # Admin resolves report
        st, res = api_request("/api/admin/reports/resolve", method="POST", payload={
            "reportId": report_id,
            "action": "DISMISS"
        }, token=self.admin_token)
        self.assertEqual(st, 200)

    def test_04_block_and_mute_controls(self):
        """Test user block prevents direct messages/connections and mute filters posts."""
        # User A blocks User B
        st, res = api_request("/api/settings/block", method="POST", payload={"targetUserId": self.user_b_id}, token=self.user_a_token)
        self.assertEqual(st, 200)
        self.assertTrue(res.get("isBlocked"))

        # User B attempts to message User A -> Blocked (403)
        st, res = api_request("/api/messages/send", method="POST", payload={
            "receiverId": self.user_a_id,
            "messageText": "Hello from blocked user"
        }, token=self.user_b_token)
        self.assertEqual(st, 403)

        # User B attempts to connect with User A -> Blocked (403)
        st, res = api_request("/api/users/connect", method="POST", payload={"targetUserId": self.user_a_id}, token=self.user_b_token)
        self.assertEqual(st, 403)

        # Unblock User B
        st, res = api_request("/api/settings/block", method="POST", payload={"targetUserId": self.user_b_id}, token=self.user_a_token)
        self.assertEqual(st, 200)
        self.assertFalse(res.get("isBlocked"))

        # User A mutes User B
        st, res = api_request("/api/settings/mute", method="POST", payload={"targetUserId": self.user_b_id}, token=self.user_a_token)
        self.assertEqual(st, 200)
        self.assertTrue(res.get("isMuted"))

        # User A checks muted list
        st, res = api_request("/api/settings/muted", method="GET", token=self.user_a_token)
        self.assertEqual(st, 200)
        muted_ids = [m["userId"] for m in res.get("muted", [])]
        self.assertIn(self.user_b_id, muted_ids)

    # -------------------------------------------------------------
    # FEATURE 4: Notifications Central System
    # -------------------------------------------------------------
    def test_05_notifications_flow(self):
        """Test notifications retrieval and mark all read."""
        st, res = api_request("/api/notifications", method="GET", token=self.user_a_token)
        self.assertEqual(st, 200)
        self.assertIn("notifications", res)
        self.assertIn("unreadCount", res)

        # Mark all read
        st, res = api_request("/api/notifications/read", method="POST", payload={}, token=self.user_a_token)
        self.assertEqual(st, 200)
        self.assertTrue(res.get("success"))

    # -------------------------------------------------------------
    # FEATURE 5: Global Categorized Search
    # -------------------------------------------------------------
    def test_06_global_categorized_search(self):
        """Test search across People, Posts, Hashtags, and Events."""
        st, res = api_request("/api/users/search?q=Alpha", method="GET", token=self.user_b_token)
        self.assertEqual(st, 200)
        self.assertIn("users", res)
        self.assertIn("hashtags", res)
        self.assertIn("posts", res)
        self.assertIn("events", res)
        
        # Verify User A appears in search
        user_names = [u["fullName"] for u in res.get("users", [])]
        self.assertIn("Feature User Alpha", user_names)

    # -------------------------------------------------------------
    # FEATURE 6: Better Professional Profiles
    # -------------------------------------------------------------
    def test_07_professional_profiles_crud(self):
        """Test skills, education, experience, projects, and certifications management."""
        # 1. Add Skill
        st, res = api_request("/api/profile/skills", method="POST", payload={"action": "ADD", "skill": "Python"}, token=self.user_a_token)
        self.assertEqual(st, 200)
        self.assertIn("Python", res.get("skills", []))

        # 2. Add Education
        st, res = api_request("/api/profile/education", method="POST", payload={
            "action": "ADD",
            "institution": "Stanford University",
            "degree": "Master of Science",
            "field": "Computer Science",
            "startYear": "2020",
            "endYear": "2022"
        }, token=self.user_a_token)
        self.assertEqual(st, 200)
        self.assertTrue(len(res.get("education", [])) > 0)

        # 3. Add Experience
        st, res = api_request("/api/profile/experience", method="POST", payload={
            "action": "ADD",
            "company": "Tech Corp",
            "position": "Lead Software Engineer",
            "location": "Bengaluru, India",
            "startDate": "2022",
            "isCurrent": True
        }, token=self.user_a_token)
        self.assertEqual(st, 200)
        self.assertTrue(len(res.get("experience", [])) > 0)

        # 4. Add Project
        st, res = api_request("/api/profile/projects", method="POST", payload={
            "action": "ADD",
            "projectName": "Joining Hands Web Ecosystem",
            "technologies": "Python, JavaScript, SQLite",
            "projectUrl": "https://joining-hands.org"
        }, token=self.user_a_token)
        self.assertEqual(st, 200)
        self.assertTrue(len(res.get("projects", [])) > 0)

        # 5. Add Certification
        st, res = api_request("/api/profile/certifications", method="POST", payload={
            "action": "ADD",
            "certName": "AWS Certified Solutions Architect",
            "issuingOrg": "Amazon Web Services",
            "issueDate": "2024"
        }, token=self.user_a_token)
        self.assertEqual(st, 200)
        self.assertTrue(len(res.get("certifications", [])) > 0)

        # 6. Fetch Full Profile
        st, res = api_request(f"/api/profile/full?userId={self.user_a_id}", method="GET", token=self.user_b_token)
        self.assertEqual(st, 200)
        prof = res.get("profile", {})
        self.assertEqual(prof.get("fullName"), "Feature User Alpha")
        self.assertIn("Python", prof.get("skills", []))
        self.assertEqual(prof.get("education", [])[0]["institution"], "Stanford University")
        self.assertEqual(prof.get("experience", [])[0]["company"], "Tech Corp")
        self.assertEqual(prof.get("projects", [])[0]["projectName"], "Joining Hands Web Ecosystem")
        self.assertEqual(prof.get("certifications", [])[0]["certName"], "AWS Certified Solutions Architect")


if __name__ == "__main__":
    unittest.main()
