#!/usr/bin/env python3
"""
Database class that implements the user opeartions and methods.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """Database class for handling user operations"""

    def __init__(self):
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.create_all(self._engine)
        self.__session = sessionmaker(bind=self._engine)()

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self.__session.add(user)
        self.__session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find user by specified attributes"""
        query = self.__session.query(User)
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError()
            query = query.filter(getattr(User, key) == value)
        user = query.first()
        if user is None:
            raise NoResultFound()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes"""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError()
            setattr(user, key, value)
        self.__session.commit()
