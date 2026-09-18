"""
===============================================================================
                        JOINING HANDS WEB ECOSYSTEM
                        Enterprise Automated Test Suite
                        File: tests/api_test.py
===============================================================================
"""

import urllib.request
import json
import unittest
import sys
import os

BASE_URL = 'http://localhost:8080'

class EnterpriseAPITestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Login and acquire auth token for protected endpoint tests."""
        login_url = f"{BASE_URL}/api/auth/login"
        payload = json.dumps({
            'email': 'member@joininghands.org',
            'password': 'demo1234'
        }).encode('utf-8')
        req = urllib.request.Request(login_url, data=payload, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            cls.token = data.get('token')
            cls.user = data.get('user')

    def get_auth_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

    def test_01_public_landing_page(self):
        req = urllib.request.Request(f'{BASE_URL}/')
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)

    def test_02_static_css_and_js(self):
        req_css = urllib.request.Request(f'{BASE_URL}/static/css/styles.css')
        with urllib.request.urlopen(req_css) as resp:
            self.assertEqual(resp.status, 200)
        req_js = urllib.request.Request(f'{BASE_URL}/static/js/script.js')
        with urllib.request.urlopen(req_js) as resp:
            self.assertEqual(resp.status, 200)

    def test_03_auth_session(self):
        req = urllib.request.Request(f'{BASE_URL}/api/auth/me', headers=self.get_auth_headers())
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get('success'))

    def test_04_timeline_feed(self):
        req = urllib.request.Request(f'{BASE_URL}/api/posts', headers=self.get_auth_headers())
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get('success'))
            self.assertIn('posts', data)

    def test_05_messaging_conversations(self):
        req = urllib.request.Request(f'{BASE_URL}/api/messages/conversations', headers=self.get_auth_headers())
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get('success'))

    def test_06_notifications_engine(self):
        req = urllib.request.Request(f'{BASE_URL}/api/notifications', headers=self.get_auth_headers())
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get('success'))

    def test_07_events_manager(self):
        req = urllib.request.Request(f'{BASE_URL}/api/events', headers=self.get_auth_headers())
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get('success'))

    def test_08_saved_items_bookmarks(self):
        req = urllib.request.Request(f'{BASE_URL}/api/posts/saved', headers=self.get_auth_headers())
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get('success'))

    def test_09_user_settings(self):
        req = urllib.request.Request(f'{BASE_URL}/api/settings', headers=self.get_auth_headers())
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get('success'))

    def test_10_analytics_dashboard(self):
        req = urllib.request.Request(f'{BASE_URL}/api/analytics', headers=self.get_auth_headers())
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get('success'))

    def test_11_workflow_bug_tracker(self):
        req = urllib.request.Request(f'{BASE_URL}/api/workflow/bugs')
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get('success'))

    def test_12_admin_overview(self):
        req = urllib.request.Request(f'{BASE_URL}/api/admin/overview', headers=self.get_auth_headers())
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertTrue(data.get('success'))

if __name__ == '__main__':
    unittest.main()
