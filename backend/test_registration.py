"""
Test user registration endpoint
"""
import requests
import json

def test_registration():
    """Test user registration with proper JSON handling"""

    url = "http://localhost:8001/api/v1/auth/register"

    # Test data
    user_data = {
        "name": "Test User",
        "email": "testuser456@example.com",
        "username": "testuser456",
        "password": "TestPass123!"
    }

    print("=" * 60)
    print("Testing User Registration")
    print("=" * 60)
    print(f"\nEndpoint: {url}")
    print(f"Data: {json.dumps(user_data, indent=2)}")
    print("\nSending request...")

    try:
        response = requests.post(
            url,
            json=user_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("\n" + "=" * 60)
            print("[SUCCESS] User registration working!")
            print("=" * 60)
            return True
        else:
            print("\n" + "=" * 60)
            print(f"[FAILED] Registration failed with status {response.status_code}")
            print("=" * 60)
            return False

    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Cannot connect to backend server")
        print("Make sure the server is running on port 8001")
        return False
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    test_registration()
