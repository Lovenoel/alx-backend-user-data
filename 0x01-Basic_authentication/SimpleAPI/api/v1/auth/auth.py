"""A module for authentification"""
from flask import request
from typing import List, TypeVar

class Auth:
    """class Auth for app authentification"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns:
          - False - path
        """
        return False
    
    def authorization_header(self, request=None) -> str:
        """
        Return:
           - None - request
        """
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
            - None
        """
        return None