"""
Skill Update Check Module
Checks and pulls latest Skill version
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from .github_api import GitHubAPI, GitHubAPIError


# Skill version info (local)
SKILL_VERSION = {
    "version": "1.0.0",
    "release_date": "2025-01-20",
    "changelog": "Initial release"
}

SKILL_REPO = "OpenClaw-Skills/learning-checkin"  # Skill code repository


class SkillUpdater:
    """Skill update management"""
    
    def __init__(self, gh_data: GitHubAPI, skill_path: str):
        """
        Initialize update manager
        
        Args:
            gh_data: GitHubAPI instance for data repository
            skill_path: Local Skill path
        """
        self.gh_data = gh_data
        self.skill_path = skill_path
        # Skill code repository API (read-only, no token needed)
        self.skill_api_url = f"https://api.github.com/repos/{SKILL_REPO}/contents"
    
    def get_local_version(self) -> Dict[str, Any]:
        """Get local version info"""
        return SKILL_VERSION
    
    def get_remote_version(self) -> Optional[Dict[str, Any]]:
        """
        Get remote version info
        
        Returns:
            Remote version info, None if fetch fails
        """
        try:
            version_data = self.gh_data.get_json(self.gh_data.get_skill_version_path())
            return version_data
        except GitHubAPIError:
            return None
    
    def check_update(self) -> Dict[str, Any]:
        """
        Check if update is available
        
        Returns:
            Update check result
        """
        local_version = self.get_local_version()
        remote_version = self.get_remote_version()
        
        if not remote_version:
            return {
                "has_update": False,
                "message": "Cannot fetch remote version info",
                "local_version": local_version["version"]
            }
        
        local_ver = local_version["version"]
        remote_ver = remote_version.get("version", "0.0.0")
        
        # Version comparison (simple string comparison, assumes semantic versioning)
        has_update = self._compare_versions(remote_ver, local_ver) > 0
        
        return {
            "has_update": has_update,
            "local_version": local_ver,
            "remote_version": remote_ver,
            "remote_changelog": remote_version.get("changelog", ""),
            "remote_release_date": remote_version.get("release_date", "")
        }
    
    def _compare_versions(self, v1: str, v2: str) -> int:
        """
        Compare version numbers
        
        Args:
            v1: Version 1
            v2: Version 2
            
        Returns:
            >0 if v1>v2, =0 if equal, <0 if v1<v2
        """
        def parse_version(v):
            try:
                return [int(x) for x in v.split(".")]
            except:
                return [0, 0, 0]
        
        parts1 = parse_version(v1)
        parts2 = parse_version(v2)
        
        for i in range(3):
            if parts1[i] > parts2[i]:
                return 1
            elif parts1[i] < parts2[i]:
                return -1
        return 0
    
    def pull_update(self) -> Dict[str, Any]:
        """
        Pull update (needs specific update logic implementation)
        
        Returns:
            Update result
        """
        check_result = self.check_update()
        
        if not check_result["has_update"]:
            return {
                "success": False,
                "message": "Already latest version",
                "version": check_result["local_version"]
            }
        
        # TODO: Implement specific update logic
        # This depends on actual deployment method
        # Possible approaches:
        # 1. Download latest code from GitHub
        # 2. Update via package manager (pip)
        # 3. Prompt user to update manually
        
        return {
            "success": True,
            "message": f"New version {check_result['remote_version']} available. Please download the latest version from the repository.",
            "old_version": check_result["local_version"],
            "new_version": check_result["remote_version"]
        }


def get_update_check_result() -> Dict[str, Any]:
    """
    Get update check result (standalone function for easy calling)
    
    Returns:
        Update check result
    """
    updater = SkillUpdater(None, os.path.dirname(os.path.dirname(__file__)))
    return updater.check_update()
