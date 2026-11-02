import pytest

from errors import EntryNotFoundError, MasterExistsError, VaultLockedError


def test_unlock_correct_password(manager):
    manager.init_master("master123")
    assert manager.unlock("master123") is True


def test_unlock_wrong_password(manager):
    manager.init_master("master123")
    assert manager.unlock("wrong123") is False


def test_init_twice_fails(manager):
    manager.init_master("master123")
    with pytest.raises(MasterExistsError):
        manager.init_master("other123")
    assert manager.unlock("master123") is True


def test_add_list_get(unlocked):
    unlocked.add_entry("github", "Tuitr", "gh_secret_1")
    assert "github" in unlocked.list_entries()
    assert unlocked.get_entry("github") == ("Tuitr", "gh_secret_1")


def test_delete(unlocked):
    unlocked.add_entry("github", "Tuitr", "gh_secret_1")
    unlocked.delete_entry("github")
    assert "github" not in unlocked.list_entries()
    with pytest.raises(EntryNotFoundError):
        unlocked.get_entry("github")


def test_no_plaintext_in_file(unlocked):
    unlocked.add_entry("github", "Tuitr", "gh_secret_1")
    content = unlocked.path.read_text(encoding="utf-8")
    assert "master123" not in content
    assert "gh_secret_1" not in content


def test_locked_vault(unlocked):
    unlocked.lock()
    with pytest.raises(VaultLockedError):
        unlocked.list_entries()
