"""
API Client for communicating with the Django backend
"""

import requests
from typing import Dict, Optional, List
from config import ENDPOINTS


class APIClient:
    """Client for making API requests to the backend"""
    
    def __init__(self):
        self.token: Optional[str] = None
        self.headers: Dict[str, str] = {}
    
    def set_token(self, token: str):
        """Set authentication token"""
        self.token = token
        self.headers = {
            'Authorization': f'Token {token}'
        }
    
    def clear_token(self):
        """Clear authentication token"""
        self.token = None
        self.headers = {}
    
    def login(self, username: str, password: str) -> Dict:
        """
        Login user and get authentication token
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            Dictionary with token and user info
        """
        try:
            response = requests.post(
                ENDPOINTS['login'],
                json={'username': username, 'password': password}
            )
            response.raise_for_status()
            data = response.json()
            
            if 'token' in data:
                self.set_token(data['token'])
            
            return {'success': True, 'data': data}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': str(e)}
    
    def signup(self, username: str, email: str, password: str) -> Dict:
        """
        Register a new user
        
        Args:
            username: Desired username
            email: User's email
            password: Desired password
            
        Returns:
            Dictionary with token and user info
        """
        try:
            response = requests.post(
                ENDPOINTS['signup'],
                json={'username': username, 'email': email, 'password': password}
            )
            response.raise_for_status()
            data = response.json()
            
            if 'token' in data:
                self.set_token(data['token'])
            
            return {'success': True, 'data': data}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': str(e)}
    
    def upload_dataset(self, file_path: str) -> Dict:
        """
        Upload a CSV file
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Dictionary with upload result
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    ENDPOINTS['upload'],
                    files=files,
                    headers=self.headers
                )
                
                if response.status_code != 201 and response.status_code != 200:
                    try:
                        error_data = response.json()
                        error_msg = error_data.get('detail', error_data.get('error', response.text))
                    except:
                        error_msg = response.text or f"HTTP {response.status_code}"
                    return {'success': False, 'error': error_msg}
                
                response.raise_for_status()
                return {'success': True, 'data': response.json()}
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('detail', error_data.get('error', str(e)))
                except:
                    error_msg = e.response.text or str(e)
            return {'success': False, 'error': error_msg}
        except IOError as e:
            return {'success': False, 'error': f'File error: {str(e)}'}
    
    def get_datasets(self) -> Dict:
        """
        Get list of all user's datasets
        
        Returns:
            Dictionary with datasets list
        """
        try:
            response = requests.get(
                ENDPOINTS['datasets'],
                headers=self.headers
            )
            response.raise_for_status()
            return {'success': True, 'data': response.json()}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': str(e)}
    
    def get_dataset_detail(self, dataset_id: int) -> Dict:
        """
        Get detailed information about a specific dataset
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            Dictionary with dataset details
        """
        try:
            url = ENDPOINTS['dataset_detail'].format(id=dataset_id)
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return {'success': True, 'data': response.json()}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': str(e)}
    
    def delete_dataset(self, dataset_id: int) -> Dict:
        """
        Delete a dataset
        
        Args:
            dataset_id: ID of the dataset to delete
            
        Returns:
            Dictionary with deletion result
        """
        try:
            url = ENDPOINTS['dataset_delete'].format(id=dataset_id)
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            return {'success': True}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': str(e)}
    
    def download_pdf(self, dataset_id: int, save_path: str) -> Dict:
        """
        Download PDF report for a dataset
        
        Args:
            dataset_id: ID of the dataset
            save_path: Path where to save the PDF
            
        Returns:
            Dictionary with download result
        """
        try:
            url = ENDPOINTS['download_pdf'].format(id=dataset_id)
            response = requests.get(url, headers=self.headers, stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return {'success': True, 'path': save_path}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': str(e)}
        except IOError as e:
            return {'success': False, 'error': f'File error: {str(e)}'}
