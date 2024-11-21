#!/usr/bin/env python3
"""
A module that defines an Auth class for the app.
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import uuid
from werkzeug.security import generate_password_hash


def _generate_uuid() -> str:
    """Generate a new UUID."""
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """Hashes a password with bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Class for managing user authentication"""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user if they do not exist"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login credentials.

        Args:
            email (str): User email.
            password (str): Plain-text password.

        Returns:
            bool: True if valid credentials, False otherwise.
        """
        try:
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.checkpw(
                    password.encode('utf-8'), user.hashed_password):
                return True
        except Exception:
            pass
        return False

    def create_session(self, email: str) -> str:
        """Create a session ID for a user based on email."""
        user = self._db.find_user_by(email=email)
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        return None

    def get_user_from_session_id(self, session_id: str):
        """Retrieve user based on session ID."""
        if session_id is None:
            return None
        return self._db.find_user_by(session_id=session_id)

    def destroy_session(self, user_id: int) -> None:
        """Remove session ID for the user."""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate password reset token."""
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError("User not found")
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password using reset token."""
        user = self._db.find_user_by(reset_token=reset_token)
        if not user:
            raise ValueError("Invalid reset token")
        hashed_password = generate_password_hash(password)
        self._db.update_user(
                user.id,
                hashed_password=hashed_password,
                reset_token=None)
