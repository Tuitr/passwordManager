import json

from config import VAULT_FILE, MIN_MASTER_LENGTH
from errors import (ValidationError, MasterExistsError, VaultNotInitializedError,
                    VaultLockedError, VaultCorruptedError)
from security import hash_password, verify_password, generate_salt, derive_key

REQUIRED_KEYS = ("master", "key_salt", "entries")


class PasswordManager:
    def __init__(self, path=VAULT_FILE):
        self.path = path
        self._key = None


    def is_initialized(self):
        return self.path.exists()

    def _load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                raise VaultCorruptedError("Файл хранилища поврежден")
        for key in REQUIRED_KEYS:
            if key not in data:
                raise VaultCorruptedError("Файл хранилища поврежден")
        return data

    def _persist(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def init_master(self, password):
        if self.is_initialized():
            raise MasterExistsError("Хранилище уже создано")
        if len(password) < MIN_MASTER_LENGTH:
            raise ValidationError(f"Пароль должен быть не короче {MIN_MASTER_LENGTH} символов")

        salt, password_hash = hash_password(password)
        data = {
            "master": {"salt": salt, "password_hash": password_hash},
            "key_salt": generate_salt(),
            "entries": {},
        }
        self._persist(data)

    def unlock(self, password):
        if not self.is_initialized():
            raise VaultNotInitializedError("Хранилище не создано, выполните --init")
        data = self._load()
        master = data["master"]
        if not verify_password(password, master["salt"], master["password_hash"]):
            return False

        self._key = derive_key(password, data["key_salt"])
        return True

    def lock(self):
        self._key = None

    def _require_unlocked(self):
        if self._key is None:
            raise VaultLockedError("Хранилище заблокировано")
