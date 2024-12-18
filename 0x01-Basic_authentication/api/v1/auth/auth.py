#!/usr/bin/env python3
"""
A module to handle  API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """A class Auth for API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if the path requires authentication """
        if path is None or excluded_paths is None:
            return True
        for excluded_path in excluded_paths:
            if path.endswith(excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the Authorization header if present """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user if authenticated """
        return None
