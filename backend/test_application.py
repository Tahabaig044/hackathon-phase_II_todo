"""
Comprehensive Application Test Suite
Tests all major endpoints and features
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8001"

def test_endpoint(name, method, url, expected_status=200, data=None, headers=None):
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)

        status = "PASS" if response.status_code == expected_status else "FAIL"
        print(f"[{status}] {name}")
        print(f"      Status: {response.status_code} (expected {expected_status})")

        if response.status_code != expected_status:
            print(f"      Response: {response.text[:200]}")

        return response.status_code == expected_status
    except Exception as e:
        print(f"[FAIL] {name}")
        print(f"      Error: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("COMPREHENSIVE APPLICATION TEST")
    print("=" * 60)
    print()

    tests_passed = 0
    tests_total = 0

    # Test 1: Health Check
    print("1. Testing Health Endpoint")
    tests_total += 1
    if test_endpoint("Health Check", "GET", f"{BASE_URL}/health"):
        tests_passed += 1
    print()

    # Test 2: Root Endpoint
    print("2. Testing Root Endpoint")
    tests_total += 1
    if test_endpoint("Root Endpoint", "GET", f"{BASE_URL}/"):
        tests_passed += 1
    print()

    # Test 3: API Documentation
    print("3. Testing API Documentation")
    tests_total += 1
    if test_endpoint("API Docs", "GET", f"{BASE_URL}/docs"):
        tests_passed += 1
    print()

    # Test 4: OpenAPI Schema
    print("4. Testing OpenAPI Schema")
    tests_total += 1
    if test_endpoint("OpenAPI Schema", "GET", f"{BASE_URL}/openapi.json"):
        tests_passed += 1
    print()

    # Test 5: Tasks Endpoint (should require auth)
    print("5. Testing Tasks Endpoint (Auth Required)")
    tests_total += 1
    if test_endpoint("Tasks List (No Auth)", "GET", f"{BASE_URL}/api/v1/tasks", expected_status=401):
        tests_passed += 1
    print()

    # Test 6: Register Endpoint
    print("6. Testing User Registration")
    tests_total += 1
    test_user = {
        "email": f"test_{int(requests.get(f'{BASE_URL}/health').elapsed.total_seconds() * 1000)}@example.com",
        "password": "TestPassword123!",
        "username": "testuser"
    }
    if test_endpoint("User Registration", "POST", f"{BASE_URL}/api/v1/auth/register",
                    expected_status=200, data=test_user):
        tests_passed += 1
    print()

    # Test 7: CORS Headers
    print("7. Testing CORS Configuration")
    tests_total += 1
    try:
        response = requests.options(f"{BASE_URL}/health", timeout=10)
        has_cors = 'access-control-allow-origin' in response.headers
        print(f"[{'PASS' if has_cors else 'FAIL'}] CORS Headers")
        print(f"      CORS Enabled: {has_cors}")
        if has_cors:
            tests_passed += 1
    except Exception as e:
        print(f"[FAIL] CORS Headers")
        print(f"      Error: {str(e)}")
    print()

    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests Passed: {tests_passed}/{tests_total}")
    print(f"Success Rate: {(tests_passed/tests_total)*100:.1f}%")
    print()

    if tests_passed == tests_total:
        print("[SUCCESS] All tests passed!")
        return 0
    else:
        print(f"[WARNING] {tests_total - tests_passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
