from datetime import datetime
from config import ROLE_USER, ROLE_ADMIN

class User:

    def __init__(self, login, password, role=ROLE_USER, createdAt = None):
        self.login = login
        self.password = password
        self.role = role
        if createdAt is None:
            createdAt = datetime.now().isoformat(timespec="seconds")
        self.createdAt = createdAt


    def isAdmin(self):
        if self.role == ROLE_ADMIN:
            return True
        return False

    def toDict(self):
        return {"login": self.login, "password": self.password, "role": self.role, "createdAt": self.createdAt}

    @classmethod
    def fromDict(cls, data):
        return cls(data["login"], data["password"], data.get("role", ROLE_USER), data.get("createdAt"))


class Entry:
    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.password = password

    def toDict(self):
        return {"name": self.name, "login": self.login, "password": self.password}

    @classmethod
    def fromDict(cls, data):
        return cls(data["name"], data["login"], data["password"])
