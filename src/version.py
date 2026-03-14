"""
Version Management for Learning Check-in
Handles version checking and update notifications
"""

import json
import urllib.request
from typing import Optional, Tuple

__version__ = "3.0.0"
__repo__ = "daizongyu/learning-checkin"


def parse_version(version_str: str) -> Tuple[int, int, int]:
    """
    Parse version string like 'v1.0.0' or '1.0.0' into tuple
    
    Args:
        version_str: Version string
        
    Returns:
        Tuple of (major, minor, patch)
    """
    try:
        # Remove 'v' or 'V' prefix
        version_str = version_str.lstrip('vV')
        parts = version_str.split('.')
        return tuple(int(p) for p in parts[:3])
    except (ValueError, AttributeError, IndexError):
        return (0, 0, 0)


def check_update(timeout: float = 2.0) -> Optional[dict]:
    """
    Check for updates from GitHub Releases
    
    Args:
        timeout: Request timeout in seconds (default 2.0)
        
    Returns:
        dict with update info if available, None otherwise
    """
    try:
        url = f"https://api.github.com/repos/{__repo__}/releases/latest"
        request = urllib.request.Request(
            url,
            headers={'User-Agent': 'Learning-Checkin'}
        )
        
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read())
            latest_version = data.get('tag_name', '')
            
            if not latest_version:
                return None
            
            current_ver = parse_version(__version__)
            latest_ver = parse_version(latest_version)
            
            if latest_ver > current_ver:
                return {
                    "available": True,
                    "latest_version": latest_version,
                    "current_version": f"v{__version__}",
                    "release_url": f"https://github.com/{__repo__}/releases/latest"
                }
    except Exception:
        # Silently fail - don't block user workflow
        pass
    
    return None


def get_version_info() -> dict:
    """Get current version information"""
    return {
        "version": f"v{__version__}",
        "repo": __repo__
    }

