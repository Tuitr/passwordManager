class Entry:
    def __init__(self, name, login, password) -> None:
        self.name = name
        self.login = login
        self.password = password

    def to_dict(self):
        return {"name": self.name, "login": self.login, "password": self.password}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["login"], data["password"])
