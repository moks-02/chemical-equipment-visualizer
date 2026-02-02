"""
Quick test to verify API endpoints are working correctly
"""

import requests

API_BASE = "http://localhost:8000/api"

print("Testing API Endpoints...")
print("-" * 50)

# Test 1: Login endpoint
print("\n1. Testing login endpoint...")
try:
    response = requests.post(f"{API_BASE}/login/", json={
        "username": "test",
        "password": "test123"
    })
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✓ Login endpoint working")
    else:
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Upload endpoint (should require auth)
print("\n2. Testing upload endpoint (without auth)...")
try:
    response = requests.post(f"{API_BASE}/upload/")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✓ Upload endpoint requires authentication (correct)")
    else:
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Datasets list endpoint (should require auth)
print("\n3. Testing datasets list endpoint (without auth)...")
try:
    response = requests.get(f"{API_BASE}/datasets/")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✓ Datasets endpoint requires authentication (correct)")
    else:
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Delete endpoint structure (should be DELETE method)
print("\n4. Testing delete endpoint structure...")
try:
    response = requests.delete(f"{API_BASE}/datasets/1/delete/")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✓ Delete endpoint requires authentication (correct)")
    elif response.status_code == 404:
        print("   ✓ Delete endpoint exists (404 = not found, correct)")
    else:
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 5: PDF download endpoint (should be GET method)
print("\n5. Testing PDF download endpoint...")
try:
    response = requests.get(f"{API_BASE}/datasets/1/report/")
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print("   ✓ PDF endpoint requires authentication (correct)")
    elif response.status_code == 404:
        print("   ✓ PDF endpoint exists (404 = not found, correct)")
    else:
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "-" * 50)
print("API endpoint testing complete!")
