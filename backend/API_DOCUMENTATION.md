# API Endpoints Documentation

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication

### Login
- **Endpoint:** `POST /api/login/`
- **Body:**
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- **Response:**
  ```json
  {
    "token": "your-auth-token",
    "user_id": 1,
    "username": "admin"
  }
  ```

## Dataset Endpoints

### Upload CSV
- **Endpoint:** `POST /api/upload/`
- **Headers:** `Authorization: Token your-auth-token`
- **Body:** `multipart/form-data` with `file` field
- **Response:**
  ```json
  {
    "message": "File uploaded and processed successfully",
    "dataset": {
      "id": 1,
      "filename": "equipment.csv",
      "upload_date": "2026-02-01T12:45:00Z",
      "summary_json": {...},
      "data_json": [...]
    }
  }
  ```

### List Datasets
- **Endpoint:** `GET /api/datasets/`
- **Headers:** `Authorization: Token your-auth-token`
- **Response:**
  ```json
  {
    "count": 3,
    "datasets": [...]
  }
  ```

### Get Dataset Detail
- **Endpoint:** `GET /api/datasets/{id}/`
- **Headers:** `Authorization: Token your-auth-token`
- **Response:**
  ```json
  {
    "id": 1,
    "filename": "equipment.csv",
    "upload_date": "2026-02-01T12:45:00Z",
    "summary_json": {...},
    "data_json": [...]
  }
  ```

### Generate PDF Report
- **Endpoint:** `POST /api/datasets/{id}/report/`
- **Headers:** `Authorization: Token your-auth-token`
- **Response:** PDF file download

### Delete Dataset
- **Endpoint:** `DELETE /api/datasets/{id}/delete/`
- **Headers:** `Authorization: Token your-auth-token`
- **Response:**
  ```json
  {
    "message": "Dataset deleted successfully"
  }
  ```

## Test Credentials
- **Username:** admin
- **Password:** admin123

## Admin Panel
- **URL:** http://127.0.0.1:8000/admin/
- **Login:** admin / admin123
