# src/services/user_service.py
from typing import Dict
from src.dao.user_dao import UserDAO

class UserError(Exception):
    pass

class UserService:
    def __init__(self):
        self.dao = UserDAO()

    def register(self, name: str, email: str) -> Dict:
        if not name.strip():
            raise UserError("Name required")
        if not email.strip():
            raise UserError("Email required")
        existing = self.dao.get_by_email(email)
        if existing:
            return existing
        return self.dao.create(name, email)
