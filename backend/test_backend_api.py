import requests
import json
import random

BASE_URL = "http://localhost:8001"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_root():
    """Test root endpoint"""
    print("\n" + "="*60)
    print("Testing Root Endpoint")
    print("="*60)
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_register():
    """Test user registration"""
    print("\n" + "="*60)
    print("Testing User Registration")
    print("="*60)

    # Generate unique email
    random_num = random.randint(1000, 9999)
    user_data = {
        "name": "Test User",
        "email": f"testuser{random_num}@example.com",
        "password": "TestPass123!"
    }

    print(f"Registering user: {user_data['email']}")
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/register",
        json=user_data
    )

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! User ID: {data['user']['id']}")
        print(f"Token: {data['token'][:50]}...")
        return data
    else:
        print(f"Error: {response.text}")
        return None

def test_login(email, password):
    """Test user login"""
    print("\n" + "="*60)
    print("Testing User Login")
    print("="*60)

    login_data = {
        "email": email,
        "password": password
    }

    print(f"Logging in as: {email}")
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json=login_data
    )

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! User ID: {data['user']['id']}")
        print(f"Token: {data['token'][:50]}...")
        return data
    else:
        print(f"Error: {response.text}")
        return None

def test_tasks(token):
    """Test task endpoints"""
    print("\n" + "="*60)
    print("Testing Task Endpoints")
    print("="*60)

    headers = {"Authorization": f"Bearer {token}"}

    # Create a task
    print("\n1. Creating a task...")
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/tasks",
        json=task_data,
        headers=headers
    )

    print(f"Status: {response.status_code}")
    if response.status_code in [200, 201]:
        task = response.json()
        print(f"Task created! ID: {task['id']}")
        task_id = task['id']

        # Get all tasks
        print("\n2. Getting all tasks...")
        response = requests.get(f"{BASE_URL}/api/v1/tasks", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            tasks = response.json()
            print(f"Found {len(tasks)} task(s)")

        # Update task
        print("\n3. Updating task...")
        update_data = {"completed": True}
        response = requests.put(
            f"{BASE_URL}/api/v1/tasks/{task_id}",
            json=update_data,
            headers=headers
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Task updated successfully!")

        # Delete task
        print("\n4. Deleting task...")
        response = requests.delete(
            f"{BASE_URL}/api/v1/tasks/{task_id}",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Task deleted successfully!")

        return True
    else:
        print(f"Error creating task: {response.text}")
        return False

def main():
    print("\n" + "="*60)
    print("BACKEND API TEST SUITE")
    print("="*60)

    # Test basic endpoints
    test_health()
    test_root()

    # Test authentication
    register_data = test_register()
    if register_data:
        email = register_data['user']['email']
        token = register_data['token']

        # Test login with the same user
        login_data = test_login(email, "TestPass123!")

        if login_data:
            # Test task operations
            test_tasks(token)

    print("\n" + "="*60)
    print("TEST SUITE COMPLETED")
    print("="*60)

if __name__ == "__main__":
    main()
