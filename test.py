import requests
import json
import time

BASE_URL = "http://localhost:8000"

test_data = {"name": "John DDoe", "email": "johndoe@example.com"}
response = requests.post(f"{BASE_URL}/store/Test", json={"value": test_data})

print("Creating a new item")
if response.ok:
    result = response.json()
    print(f"Created item with key: TEST")
    print(f"Response: {json.dumps(result, indent=2)}")
else:
    print(f"Failed to create item: {response.status_code}")
    print(f"Error: {response.text}")

print("Retrieving the item")
response = requests.get(f"{BASE_URL}/store/Test")

if response.ok:
    result = response.json()
    print(f"Retrieved item with key: Test")
    print(f"Response: {json.dumps(result, indent=2)}")
else:
    print(f"Failed to retrieve item: {response.status_code}")
    print(f"Error: {response.text}")

print("Updating the item")
updated_data = test_data.copy()
updated_data["email"] = "newemail"

response = requests.post(f"{BASE_URL}/store/Test", json={"value": updated_data})

if response.ok:
    result = response.json()
    print(f"Updated item with key: Test")
    print(f"Response: {json.dumps(result, indent=2)}")
else:
    print(f"Failed to update item: {response.status_code}")
    print(f"Error: {response.text}")

print("Deleting the item")
response = requests.delete(f"{BASE_URL}/store/Test")

if response.ok:
    print(f"Deleted item with key: Test")
else:
    print(f"Failed to delete item: {response.status_code}")
    print(f"Error: {response.text}")

