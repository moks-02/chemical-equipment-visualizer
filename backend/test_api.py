"""
Test script to verify all API endpoints are working correctly.
Run this after starting the Django server.
"""
import requests
import json
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000/api"

def test_login():
    """Test login endpoint"""
    print("\n1. Testing Login...")
    url = f"{BASE_URL}/login/"
    data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        token = response.json().get('token')
        print(f"✓ Login successful! Token: {token[:20]}...")
        return token
    else:
        print(f"✗ Login failed: {response.status_code}")
        print(response.text)
        return None

def test_upload_csv(token):
    """Test CSV upload endpoint"""
    print("\n2. Testing CSV Upload...")
    url = f"{BASE_URL}/upload/"
    headers = {"Authorization": f"Token {token}"}
    
    # Create sample CSV content
    csv_content = """Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-A1,Reactor,150.5,25.3,120.0
Pump-B2,Pump,200.0,35.0,80.0
Heat Exchanger-C3,Heat Exchanger,180.0,20.5,150.0"""
    
    files = {'file': ('test_equipment.csv', csv_content, 'text/csv')}
    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 201:
        data = response.json()
        dataset_id = data['dataset']['id']
        print(f"✓ Upload successful! Dataset ID: {dataset_id}")
        print(f"  Total count: {data['dataset']['summary_json']['total_count']}")
        print(f"  Avg Flowrate: {data['dataset']['summary_json']['avg_flowrate']}")
        return dataset_id
    else:
        print(f"✗ Upload failed: {response.status_code}")
        print(response.text)
        return None

def test_list_datasets(token):
    """Test list datasets endpoint"""
    print("\n3. Testing List Datasets...")
    url = f"{BASE_URL}/datasets/"
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ List successful! Found {data['count']} dataset(s)")
        for dataset in data['datasets']:
            print(f"  - {dataset['filename']} (ID: {dataset['id']})")
        return True
    else:
        print(f"✗ List failed: {response.status_code}")
        return False

def test_get_dataset_detail(token, dataset_id):
    """Test get dataset detail endpoint"""
    print(f"\n4. Testing Get Dataset Detail (ID: {dataset_id})...")
    url = f"{BASE_URL}/datasets/{dataset_id}/"
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Detail retrieved successfully!")
        print(f"  Filename: {data['filename']}")
        print(f"  Data rows: {len(data['data_json'])}")
        return True
    else:
        print(f"✗ Detail retrieval failed: {response.status_code}")
        return False

def test_generate_report(token, dataset_id):
    """Test PDF report generation"""
    print(f"\n5. Testing Generate PDF Report (ID: {dataset_id})...")
    url = f"{BASE_URL}/datasets/{dataset_id}/report/"
    headers = {"Authorization": f"Token {token}"}
    
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        # Save PDF
        with open(f"test_report_{dataset_id}.pdf", 'wb') as f:
            f.write(response.content)
        print(f"✓ PDF generated successfully! Saved as test_report_{dataset_id}.pdf")
        print(f"  Size: {len(response.content)} bytes")
        return True
    else:
        print(f"✗ PDF generation failed: {response.status_code}")
        return False

def run_tests():
    """Run all tests"""
    print("="*60)
    print("Chemical Equipment Visualizer API Test Suite")
    print("="*60)
    
    # Test 1: Login
    token = test_login()
    if not token:
        print("\n✗ Cannot proceed without authentication token")
        return
    
    # Test 2: Upload CSV
    dataset_id = test_upload_csv(token)
    if not dataset_id:
        print("\n✗ Cannot proceed without dataset ID")
        return
    
    # Test 3: List Datasets
    test_list_datasets(token)
    
    # Test 4: Get Dataset Detail
    test_get_dataset_detail(token, dataset_id)
    
    # Test 5: Generate PDF Report
    test_generate_report(token, dataset_id)
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)

if __name__ == "__main__":
    try:
        run_tests()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to server.")
        print("  Make sure Django server is running: python manage.py runserver")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
