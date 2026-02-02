# User-Specific Dataset History

## Changes Implemented

### Database Model Updates
- Added `user` foreign key to `UploadedDataset` model
- Updated model to maintain last 5 datasets **per user** (instead of globally)
- Created and applied migration `0002_uploadeddataset_user.py`

### Backend API Updates
All dataset-related endpoints now filter by the authenticated user:

1. **Upload CSV** (`POST /api/upload/`)
   - Associates uploaded dataset with `request.user`
   
2. **List Datasets** (`GET /api/datasets/`)
   - Returns only the current user's last 5 datasets
   
3. **Get Dataset Detail** (`GET /api/datasets/<id>/`)
   - Only returns dataset if it belongs to current user
   
4. **Generate Report** (`POST /api/datasets/<id>/report/`)
   - Only generates reports for user's own datasets
   
5. **Preview Report** (`GET /api/datasets/<id>/preview/`)
   - Only previews user's own datasets
   
6. **Delete Dataset** (`DELETE /api/datasets/<id>/delete/`)
   - Only deletes user's own datasets

### Security Benefits
- **Data Isolation**: Users can only view, download, and delete their own datasets
- **Privacy**: No user can access another user's uploaded data
- **Resource Management**: Each user has their own 5-dataset limit

### Frontend Impact
- No frontend changes required
- Existing React app automatically works with user-specific data
- Login/signup system ensures proper user authentication

## Testing Instructions
1. Create multiple user accounts using the signup feature
2. Upload CSV files as different users
3. Verify each user only sees their own upload history
4. Confirm users cannot access other users' datasets by manipulating IDs
