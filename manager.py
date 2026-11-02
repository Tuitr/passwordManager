import json

from cryptography.fernet import InvalidToken

from config import MIN_MASTER_LENGTH, VAULT_FILE
from errors import (
    EntryExistsError,
    EntryNotFoundError,
    MasterExistsError,
    ValidationError,
    VaultCorruptedError,
    VaultLockedError,
    VaultNotInitializedError,
)
from models import Entry
from security import decrypt, derive_key, encrypt, generate_salt, hash_password, verify_password

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
            raise VaultNotInitializedError("Хранилище не создано, сначала создайте его")
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

    def add_entry(self, name, login, pwd):
        self._require_unlocked()
        name = name.strip()
        if not name or not pwd:
            raise ValidationError("Название и пароль не могут быть пустыми")
        data = self._load()
        if name in data["entries"]:
            raise EntryExistsError(f"Запись {name} уже есть")
        entry = Entry(name, login, encrypt(self._key, pwd))
        data["entries"][name] = entry.to_dict()
        self._persist(data)

    def list_entries(self):
        self._require_unlocked()
        data = self._load()
        return sorted(data["entries"].keys())

    def get_entry(self, name):
        self._require_unlocked()
        data = self._load()
        if name not in data["entries"]:
            raise EntryNotFoundError(f"Запись {name} не найдена")
        entry = Entry.from_dict(data["entries"][name])
        try:
            password = decrypt(self._key, entry.password)
        except InvalidToken:
            raise VaultCorruptedError("Не удалось расшифровать запись")
        return entry.login, password

    def delete_entry(self, name):
        self._require_unlocked()
        data = self._load()
        if name not in data["entries"]:
            raise EntryNotFoundError(f"Запись {name} не найдена")
        del data["entries"][name]
        self._persist(data)
