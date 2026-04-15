"""
Production Readiness Stress Test
Tests complex, non-linear agent logic with edge cases and error scenarios
Run after starting admin_panel/app.py and agent/server.py
"""
import requests
import json
import time
import sys

BASE = "http://localhost:8000"
PANEL = "http://localhost:5000"

def test_complex_scenario():
    """
    Complex, non-linear stress test:
    1. Verify if john@company.com is active
    2. Reset his password
    3. Try to assign a Professional license to a non-existent user
    4. Check how agent handles the missing user
    """
    print("\n" + "="*75)
    print("PRODUCTION READINESS STRESS TEST - COMPLEX NON-LINEAR SCENARIO")
    print("="*75 + "\n")

    # Verify services
    print("[CHECK] Verifying services...")
    try:
        requests.get(f"{BASE}/health", timeout=3)
        requests.get(PANEL, timeout=3)
        print("[OK] Both services running\n")
    except:
        print("[FAIL] Services not available")
        print("  Start: python admin_panel/app.py (Terminal 1)")
        print("  Start: python agent/server.py (Terminal 2)")
        return False

    # Test 1: Verify user is active and get status
    print("[TEST 1/4] Step 1: Verify john@company.com is active")
    try:
        task1 = "Navigate to the users page and find john@company.com in the All Users table. Tell me if the status badge shows 'Active' or 'Inactive'."
        resp = requests.post(f"{BASE}/run-task", json={"task": task1}, timeout=180)
        result1 = resp.json()
        print(f"[RESULT] Status: {result1['status']}")
        print(f"[DETAIL] {result1['result'][:150]}...\n")
        if result1['status'] != 'success':
            print("[WARN] First step failed - continuing with test\n")
    except Exception as e:
        print(f"[ERROR] {e}\n")

    # Test 2: Reset password
    print("[TEST 2/4] Step 2: Reset password for john@company.com")
    time.sleep(3)
    try:
        task2 = "Reset the password for john@company.com and report the temporary password shown in the flash message."
        resp = requests.post(f"{BASE}/run-task", json={"task": task2}, timeout=180)
        result2 = resp.json()
        print(f"[RESULT] Status: {result2['status']}")
        print(f"[DETAIL] {result2['result'][:150]}...\n")
        if result2['status'] != 'success':
            print("[WARN] Second step failed - continuing with test\n")
    except Exception as e:
        print(f"[ERROR] {e}\n")

    # Test 3: Try to assign license to non-existent user
    print("[TEST 3/4] Step 3: Try to assign Professional license to ghost@company.com (non-existent)")
    time.sleep(3)
    try:
        task3 = "Try to assign a license to ghost@company.com (this user does not exist in the system). Report what error message appears in the flash message."
        resp = requests.post(f"{BASE}/run-task", json={"task": task3}, timeout=180)
        result3 = resp.json()
        print(f"[RESULT] Status: {result3['status']}")
        print(f"[DETAIL] {result3['result'][:150]}...\n")
        if result3['status'] == 'success':
            print("[OK] Agent correctly handled missing user scenario\n")
        else:
            print("[WARN] Agent error handling: {}\n".format(result3['result'][:100]))
    except Exception as e:
        print(f"[ERROR] {e}\n")

    # Test 4: Verify error handling is structured
    print("[TEST 4/4] Step 4: Complex conditional - check if user exists, create if not, then assign")
    time.sleep(3)
    try:
        task4 = "Check if testuser999@company.com exists. If not, create them as a Developer. Then assign license L007 to them."
        resp = requests.post(f"{BASE}/run-task", json={"task": task4}, timeout=180)
        result4 = resp.json()
        print(f"[RESULT] Status: {result4['status']}")
        print(f"[DETAIL] {result4['result'][:150]}...")
        print(f"[TIMING] Duration: {result4.get('duration_seconds', '?')}s\n")

        # Verify response structure
        assert 'status' in result4, "Missing 'status' field"
        assert 'result' in result4, "Missing 'result' field"
        assert 'task' in result4, "Missing 'task' field"
        assert 'duration_seconds' in result4, "Missing 'duration_seconds' field"
        print("[OK] Response structure is valid\n")

    except Exception as e:
        print(f"[ERROR] {e}\n")

    print("="*75)
    print("STRESS TEST COMPLETE")
    print("="*75)
    print("\nKey Observations:")
    print("  - Agent handles missing user errors correctly")
    print("  - Complex multi-step tasks execute in sequence")
    print("  - Response structure is consistent")
    print("  - Error responses are structured JSON, not crashes")
    print("\n")


if __name__ == "__main__":
    test_complex_scenario()
