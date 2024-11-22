#!/usr/bin/env python3
"""
A module that handles basic authentication.
"""
from typing import TypeVar, Optional
import base64
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class to handle Basic Authentication
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> Optional[str]:
        """
        Extracts the Base64 part of the Authorization header for Basic Authentication.

        Args:
            authorization_header (str): The authorization header to extract the base64 part from.

        Returns:
            Optional[str]: The Base64 string after "Basic " if the header is valid, None otherwise.
        """
        if authorization_header is None or not isinstance(
            authorization_header, str):
            return None
        if authorization_header.startswith("Basic "):
            return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> Optional[str]:
        """
        Decodes a Base64 string to a UTF-8 string.

        Args:
            base64_authorization_header (str): The Base64 encoded string to decode.

        Returns:
            Optional[str]: The decoded string if valid Base64, None otherwise.
        """
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header).decode('utf-8')
            return decoded
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Optional[tuple[str, str]]:
        """
        Extracts the email and password from a decoded Base64 authorization string.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64 authorization header.

        Returns:
            Optional[tuple[str, str]]: A tuple with email and password if valid, None otherwise.
        """
        if decoded_base64_authorization_header is None or not isinstance(
            decoded_base64_authorization_header, str):
            return None, None
        if ':' in decoded_base64_authorization_header:
            email, password = decoded_base64_authorization_header.split(':', 1)
            return email, password
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> Optional[TypeVar('User')]:
        """
        Retrieves the User instance based on the provided email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            Optional[User]: The User instance if credentials are valid, None otherwise.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        user = User.search(email=user_email)
        if user is None or not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """
        Retrieves the current authenticated user based on the request's Authorization header.

        Args:
            request (flask.Request): The Flask request object (optional).

        Returns:
            Optional[User]: The authenticated User object or None if authentication fails.
        """
        authorization_header = request.headers.get("Authorization") if request else None
        if not authorization_header:
            return None

        base64_authorization_header = self.extract_base64_authorization_header(
            authorization_header
            )
        if not base64_authorization_header:
            return None

        decoded_authorization_header = self.decode_base64_authorization_header(
            base64_authorization_header
            )
        if not decoded_authorization_header:
            return None

        user_email, user_pwd = self.extract_user_credentials(
            decoded_authorization_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(
            user_email, user_pwd)
