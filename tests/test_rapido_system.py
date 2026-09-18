"""
The Group of Joining Hands - Rapido Sub-System Automated Integration Test Suite
=============================================================================
Tests the Rapido ride booking system and driver dashboard:
1. DB schema checks (rapido_rides and rapido_driver_stats exist)
2. Ride Booking API flow (booking, active state, completion)
3. Driver Mode API flow (toggling online, updating driver metrics)
4. Authentication & Security guards on Rapido endpoints
"""

import unittest
import os
import json
import time
import urllib.request
import urllib.error
import sqlite3

from app.config.config import PORT
from app.database.db import get_db, init_db

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
        try:
            return e.code, json.loads(e.read().decode("utf-8"))
        except Exception:
            return e.code, {}


class TestRapidoSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize db
        init_db()
        
        # Create a fresh test user
        cls.ts = int(time.time() * 1000)
        cls.user_email = f"rapido_test_{cls.ts}@joininghands.org"
        
        # Sign up user
        st, res = api_request("/api/auth/signup", method="POST", payload={
            "fullName": "Rapido Tester",
            "email": cls.user_email,
            "password": "Password123!",
            "headline": "QA Engineer"
        })
        cls.token = res.get("token")
        cls.user_id = res.get("user", {}).get("id")

    # -------------------------------------------------------------
    # 1. DATABASE SCHEMA VERIFICATION
    # -------------------------------------------------------------
    def test_01_database_schema_exists(self):
        """Verify that the rapido_rides and rapido_driver_stats tables exist in SQLite."""
        conn = get_db()
        cursor = conn.cursor()
        
        # Check rapido_rides
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rapido_rides'")
        self.assertIsNotNone(cursor.fetchone(), "rapido_rides table should be created.")
        
        # Check rapido_driver_stats
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rapido_driver_stats'")
        self.assertIsNotNone(cursor.fetchone(), "rapido_driver_stats table should be created.")
        
        conn.close()

    # -------------------------------------------------------------
    # 2. SECURITY & AUTHENTICATION GUARDS
    # -------------------------------------------------------------
    def test_02_auth_guards(self):
        """Verify that endpoints reject unauthenticated requests with 401."""
        endpoints = [
            ("/api/rapido/rides", "GET", None),
            ("/api/rapido/driver/stats", "GET", None),
            ("/api/rapido/book", "POST", {"pickup": "MG Road", "dropoff": "Koramangala", "vehicle_type": "BIKE", "fare": 48.0}),
            ("/api/rapido/complete", "POST", {"ride_id": 1, "status": "COMPLETED"}),
            ("/api/rapido/driver/toggle", "POST", {"is_online": True}),
            ("/api/rapido/driver/add-earning", "POST", {"fare": 48.0})
        ]
        
        for path, method, payload in endpoints:
            st, res = api_request(path, method=method, payload=payload, token=None)
            self.assertEqual(st, 401, f"{method} {path} should require authentication.")

    # -------------------------------------------------------------
    # 3. RIDER BOOKING & RIDE HISTORY WORKFLOW
    # -------------------------------------------------------------
    def test_03_booking_and_history_workflow(self):
        """Verify user booking flow, data persistence, and completion feedback logs."""
        # Step A: Attempt to book with missing fields (should return 400)
        st, res = api_request("/api/rapido/book", method="POST", payload={
            "pickup": "",
            "dropoff": "MG Road",
            "vehicle_type": "BIKE"
        }, token=self.token)
        self.assertEqual(st, 400)
        
        # Step B: Book a valid ride
        st, res = api_request("/api/rapido/book", method="POST", payload={
            "pickup": "Koramangala",
            "dropoff": "MG Road",
            "vehicle_type": "BIKE",
            "fare": 54.0
        }, token=self.token)
        self.assertEqual(st, 200)
        self.assertTrue(res.get("success"))
        
        ride_id = res.get("ride_id")
        otp = res.get("otp")
        captain = res.get("captain", {})
        
        self.assertIsNotNone(ride_id)
        self.assertIsNotNone(otp)
        self.assertIn(captain.get("name"), ['Siddharth M.', 'Ramesh G.', 'Mohan K.', 'Anand S.', 'Karan P.'])
        
        # Step C: Retrieve user ride history
        st, res = api_request("/api/rapido/rides", method="GET", token=self.token)
        self.assertEqual(st, 200)
        self.assertTrue(res.get("success"))
        rides = res.get("rides", [])
        self.assertGreaterEqual(len(rides), 1)
        self.assertEqual(rides[0]["id"], ride_id)
        self.assertEqual(rides[0]["pickup"], "Koramangala")
        self.assertEqual(rides[0]["dropoff"], "MG Road")
        self.assertEqual(rides[0]["status"], "PENDING")
        
        # Step D: Complete the ride with feedback rating
        st, res = api_request("/api/rapido/complete", method="POST", payload={
            "ride_id": ride_id,
            "status": "COMPLETED",
            "rating": 5,
            "comments": "Safe ride, polite captain!"
        }, token=self.token)
        self.assertEqual(st, 200)
        self.assertTrue(res.get("success"))
        
        # Step E: Verify updated history reflects feedback
        st, res = api_request("/api/rapido/rides", method="GET", token=self.token)
        rides = res.get("rides", [])
        self.assertEqual(rides[0]["status"], "COMPLETED")
        self.assertEqual(rides[0]["rating"], 5)
        self.assertEqual(rides[0]["comments"], "Safe ride, polite captain!")

    # -------------------------------------------------------------
    # 4. CAPTAIN MODE WORKFLOW (DRIVER PORTAL)
    # -------------------------------------------------------------
    def test_04_driver_dashboard_and_earnings(self):
        """Verify Captain Mode stats toggle, online statuses, and dynamic earnings calculations."""
        # Step A: Fetch driver stats (should auto-create driver record)
        st, res = api_request("/api/rapido/driver/stats", method="GET", token=self.token)
        self.assertEqual(st, 200)
        self.assertTrue(res.get("success"))
        stats = res.get("stats", {})
        self.assertFalse(stats.get("is_online"))
        self.assertEqual(stats.get("total_earnings"), 0.0)
        self.assertEqual(stats.get("total_rides"), 0)
        
        # Step B: Toggle online status to true
        st, res = api_request("/api/rapido/driver/toggle", method="POST", payload={"is_online": True}, token=self.token)
        self.assertEqual(st, 200)
        self.assertTrue(res.get("is_online"))
        
        # Step C: Log a driver ride earning
        st, res = api_request("/api/rapido/driver/add-earning", method="POST", payload={"fare": 65.50}, token=self.token)
        self.assertEqual(st, 200)
        self.assertTrue(res.get("success"))
        
        # Step D: Fetch stats again to check updated values
        st, res = api_request("/api/rapido/driver/stats", method="GET", token=self.token)
        self.assertEqual(st, 200)
        stats = res.get("stats", {})
        self.assertEqual(stats.get("total_earnings"), 65.50)
        self.assertEqual(stats.get("total_rides"), 1)

    # -------------------------------------------------------------
    # 5. PEER-TO-PEER INTERACTIVE COORDINATION & CHAT WORKFLOW
    # -------------------------------------------------------------
    def test_05_peer_to_peer_workflow(self):
        """Verify the full peer-to-peer booking, accepting, coordinate tracking, and chat lifecycle."""
        # Create a second user (Captain)
        ts2 = int(time.time() * 1000) + 1
        captain_email = f"rapido_captain_{ts2}@joininghands.org"
        st, res = api_request("/api/auth/signup", method="POST", payload={
            "fullName": "Captain Hero",
            "email": captain_email,
            "password": "Password123!",
            "headline": "Professional Captain"
        })
        captain_token = res.get("token")
        self.assertIsNotNone(captain_token)
        
        # Step A: Rider (self.token) books a ride
        st, res = api_request("/api/rapido/book", method="POST", payload={
            "pickup": "Indiranagar",
            "dropoff": "Whitefield",
            "vehicle_type": "AUTO",
            "fare": 75.0
        }, token=self.token)
        self.assertEqual(st, 200)
        ride_id = res.get("ride_id")
        otp = res.get("otp")
        self.assertIsNotNone(ride_id)
        self.assertIsNotNone(otp)
        
        # Step B: Captain polls for offers
        st, res = api_request("/api/rapido/driver/offers", method="GET", token=captain_token)
        self.assertEqual(st, 200)
        offers = res.get("offers", [])
        self.assertGreaterEqual(len(offers), 1)
        self.assertEqual(offers[0]["id"], ride_id)
        
        # Step C: Captain accepts the ride
        st, res = api_request("/api/rapido/driver/accept", method="POST", payload={
            "ride_id": ride_id
        }, token=captain_token)
        self.assertEqual(st, 200)
        
        # Step D: Rider checks ride status, verifies driver info is assigned
        st, res = api_request(f"/api/rapido/ride-status?ride_id={ride_id}", method="GET", token=self.token)
        self.assertEqual(st, 200)
        ride = res.get("ride", {})
        self.assertEqual(ride["status"], "ACCEPTED")
        self.assertEqual(ride["captain_name"], "Captain Hero")
        
        # Step E: Captain updates coords
        st, res = api_request("/api/rapido/driver/update-coords", method="POST", payload={
            "ride_id": ride_id,
            "x": 420.5,
            "y": 180.2,
            "angle": 1.57
        }, token=captain_token)
        self.assertEqual(st, 200)
        
        # Step F: Chat messaging exchange
        st, res = api_request("/api/rapido/chat/send", method="POST", payload={
            "ride_id": ride_id,
            "message": "Hi, standing near the gate."
        }, token=self.token)
        self.assertEqual(st, 200)
        
        st, res = api_request("/api/rapido/chat/send", method="POST", payload={
            "ride_id": ride_id,
            "message": "Yes, coming."
        }, token=captain_token)
        self.assertEqual(st, 200)
        
        st, res = api_request(f"/api/rapido/chat/messages?ride_id={ride_id}", method="GET", token=self.token)
        self.assertEqual(st, 200)
        messages = res.get("messages", [])
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["message"], "Hi, standing near the gate.")
        self.assertEqual(messages[1]["message"], "Yes, coming.")
        
        # Step G: Captain arrives at pickup
        st, res = api_request("/api/rapido/driver/update-status", method="POST", payload={
            "ride_id": ride_id,
            "status": "ARRIVED_PICKUP"
        }, token=captain_token)
        self.assertEqual(st, 200)
        
        # Step H: Captain starts the ride with OTP
        st, res = api_request("/api/rapido/driver/update-status", method="POST", payload={
            "ride_id": ride_id,
            "status": "IN_PROGRESS",
            "otp": otp
        }, token=captain_token)
        self.assertEqual(st, 200)
        
        # Step I: Captain completes the ride
        st, res = api_request("/api/rapido/driver/update-status", method="POST", payload={
            "ride_id": ride_id,
            "status": "COMPLETED"
        }, token=captain_token)
        self.assertEqual(st, 200)


if __name__ == '__main__':
    unittest.main()
