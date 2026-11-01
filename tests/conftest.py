import pytest

from manager import PasswordManager


@pytest.fixture(autouse=True)
def fast_hashing(monkeypatch):
    monkeypatch.setattr("security.HASH_ITERATIONS", 1000)


@pytest.fixture
def manager(tmp_path):
    return PasswordManager(tmp_path / "vault.json")


@pytest.fixture
def unlocked(manager):
    manager.init_master("master123")
    manager.unlock("master123")
    return manager