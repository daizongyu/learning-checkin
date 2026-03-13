"""
GitHub API Wrapper Module
Handles all data interaction with GitHub repository
"""

import base64
import json
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
import requests


class GitHubAPI:
    """GitHub API client, handles authentication, read/write, conflict retry"""
    
    def __init__(self, token: str, repo: str):
        """
        Initialize GitHub API client
        
        Args:
            token: GitHub Personal Access Token
            repo: Repository path, format "username/repo"
        """
        self.token = token
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{repo}/contents"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _get_file(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Get file content and SHA
        
        Args:
            path: File path (relative to repository root)
            
        Returns:
            Dictionary with content, sha, size, etc. Returns None if not exists
        """
        url = f"{self.base_url}/{path}"
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            
            # Decode content
            if data.get("content"):
                data["decoded_content"] = base64.b64decode(data["content"]).decode("utf-8")
            
            return data
        except requests.exceptions.RequestException as e:
            raise GitHubAPIError(f"Failed to read file {path}: {str(e)}")
    
    def get_file_content(self, path: str) -> Optional[str]:
        """
        Get file content as string
        
        Args:
            path: File path
            
        Returns:
            File content string, None if not exists
        """
        result = self._get_file(path)
        return result["decoded_content"] if result else None
    
    def get_json(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Get JSON file content and parse
        
        Args:
            path: File path
            
        Returns:
            Parsed dictionary, None if not exists or parse fails
        """
        content = self.get_file_content(path)
        if content is None:
            return None
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise GitHubAPIError(f"JSON parse error {path}: {str(e)}")
    
    def _put_file(self, path: str, content: str, message: str, sha: Optional[str] = None) -> Dict[str, Any]:
        """
        Write file
        
        Args:
            path: File path
            content: File content
            message: Commit message
            sha: File SHA (required when updating existing file)
            
        Returns:
            GitHub API response
        """
        url = f"{self.base_url}/{path}"
        data = {
            "message": message,
            "content": base64.b64encode(content.encode("utf-8")).decode("utf-8")
        }
        if sha:
            data["sha"] = sha
        
        try:
            # PUT method for create or update
            response = self.session.put(url, json=data, timeout=10)
            
            if response.status_code in [200, 201]:
                return response.json()
            elif response.status_code == 409:
                raise GitHubConflictError(f"Write conflict {path}")
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise GitHubAPIError(f"Failed to write file {path}: {str(e)}")
    
    def put_file(self, path: str, content: str, message: str, sha: Optional[str] = None, 
                 max_retries: int = 3) -> Dict[str, Any]:
        """
        Write file with retry mechanism
        
        Args:
            path: File path
            content: File content
            message: Commit message
            sha: File SHA (required when updating existing file)
            max_retries: Maximum retry attempts
            
        Returns:
            GitHub API response
        """
        for attempt in range(max_retries):
            try:
                return self._put_file(path, content, message, sha)
            except GitHubConflictError:
                if attempt == max_retries - 1:
                    raise
                # Wait and retry
                time.sleep(0.5 * (attempt + 1))
        raise GitHubAPIError("Write failed, max retries reached")
    
    def put_json(self, path: str, data: Dict[str, Any], message: str, 
                 sha: Optional[str] = None, max_retries: int = 3) -> Dict[str, Any]:
        """
        Write JSON file with retry mechanism
        
        Args:
            path: File path
            data: Dictionary data
            message: Commit message
            sha: File SHA
            max_retries: Maximum retry attempts
            
        Returns:
            GitHub API response
        """
        content = json.dumps(data, ensure_ascii=False, indent=2)
        return self.put_file(path, content, message, sha, max_retries)
    
    def update_json_with_retry(self, path: str, update_func, message: str, 
                               max_retries: int = 5) -> Dict[str, Any]:
        """
        Update JSON file (automatically handles read-modify-write loop and conflicts)
        
        Args:
            path: File path
            update_func: Update function, receives current data, returns new data
            message: Commit message
            max_retries: Maximum retry attempts
            
        Returns:
            GitHub API response
        """
        for attempt in range(max_retries):
            try:
                # Read current file
                file_data = self._get_file(path)
                sha = file_data["sha"] if file_data else None
                current_data = json.loads(file_data["decoded_content"]) if file_data and file_data.get("decoded_content") else {}
                
                # Apply update
                new_data = update_func(current_data)
                
                # Write
                return self.put_json(path, new_data, message, sha)
            except GitHubConflictError:
                if attempt == max_retries - 1:
                    raise
                # Wait and retry
                time.sleep(0.5 * (attempt + 1))
            except Exception as e:
                raise GitHubAPIError(f"Update failed {path}: {str(e)}")
        
        raise GitHubAPIError("Update failed, max retries reached")
    
    def file_exists(self, path: str) -> bool:
        """Check if file exists"""
        return self._get_file(path) is not None
    
    def get_user_id_path(self, user_id: str) -> str:
        """Get user directory path"""
        return f"users/{user_id}"
    
    def get_profile_path(self, user_id: str) -> str:
        """Get user profile file path"""
        return f"users/{user_id}/profile.json"
    
    def get_streak_path(self, user_id: str) -> str:
        """Get user streak file path"""
        return f"users/{user_id}/streak.json"
    
    def get_checkin_path(self, user_id: str, date: str) -> str:
        """Get check-in file path"""
        return f"users/{user_id}/checkins/{date}.json"
    
    def get_leaderboard_path(self) -> str:
        """Get leaderboard file path"""
        return "leaderboard/current.json"
    
    def get_skill_version_path(self) -> str:
        """Get Skill version file path"""
        return "skill/version.json"


class GitHubAPIError(Exception):
    """GitHub API error"""
    pass


class GitHubConflictError(GitHubAPIError):
    """GitHub write conflict error (SHA mismatch)"""
    pass
