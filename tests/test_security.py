import string

import pytest
from cryptography.fernet import InvalidToken

from security import (hash_password, verify_password, generate_salt,
                      derive_key, encrypt, decrypt, generate_password)


def test_verify_password():
    salt, password_hash = hash_password("master123")
    assert verify_password("master123", salt, password_hash) is True
    assert verify_password("wrong123", salt, password_hash) is False


def test_salt_is_random():
    salt1, hash1 = hash_password("master123")
    salt2, hash2 = hash_password("master123")
    assert salt1 != salt2
    assert hash1 != hash2


def test_encrypt_decrypt():
    key = derive_key("master123", generate_salt())
    token = encrypt(key, "secret")
    assert token != "secret"
    assert decrypt(key, token) == "secret"


def test_wrong_key():
    salt = generate_salt()
    token = encrypt(derive_key("master123", salt), "secret")
    with pytest.raises(InvalidToken):
        decrypt(derive_key("wrong123", salt), token)


def test_generate_password():
    password = generate_password(20)
    assert len(password) == 20
    assert any(c.islower() for c in password)
    assert any(c.isupper() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(c in string.punctuation for c in password)


def test_generate_too_short():
    with pytest.raises(ValueError):
        generate_password(3)