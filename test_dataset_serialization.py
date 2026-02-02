"""
Test to verify dataset serialization is working correctly
"""

import requests
import json

API_BASE = "http://localhost:8000/api"

print("Testing Dataset Serialization...")
print("-" * 50)

# First, we need to login to get a token
print("\n1. Logging in...")
login_response = requests.post(f"{API_BASE}/login/", json={
    "username": "admin",  # Try common username
    "password": "admin"
})

if login_response.status_code != 200:
    print("   Note: Login with 'admin/admin' failed, which is expected if not created yet")
    print("   You can test by logging in through the desktop app first")
else:
    token = login_response.json().get('token')
    headers = {'Authorization': f'Token {token}'}
    
    # Test getting datasets
    print("\n2. Fetching datasets list...")
    datasets_response = requests.get(f"{API_BASE}/datasets/", headers=headers)
    
    if datasets_response.status_code == 200:
        datasets = datasets_response.json()
        print(f"   ✓ Found {len(datasets)} dataset(s)")
        
        if datasets:
            print("\n3. Dataset details:")
            for dataset in datasets:
                print(f"\n   Dataset ID: {dataset.get('id')}")
                print(f"   Filename: {dataset.get('filename')}")
                print(f"   Upload Date: {dataset.get('upload_date')}")
                print(f"   Entry Count: {dataset.get('entry_count')}")
                
                # Check if all fields are present
                missing_fields = []
                if not dataset.get('upload_date'):
                    missing_fields.append('upload_date')
                if dataset.get('entry_count') is None:
                    missing_fields.append('entry_count')
                
                if missing_fields:
                    print(f"   ⚠ Missing fields: {', '.join(missing_fields)}")
                else:
                    print(f"   ✓ All required fields present")
        else:
            print("   No datasets found. Upload a CSV through the app to test.")
    else:
        print(f"   Error: {datasets_response.status_code}")
        print(f"   {datasets_response.text}")

print("\n" + "-" * 50)
