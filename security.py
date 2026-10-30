import hashlib
import hmac
import secrets

from config import HASH_ITERATIONS

SALT_SIZE = 16


def _compute_hash(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        HASH_ITERATIONS,
    )


def hash_password(password):
    salt = secrets.token_bytes(SALT_SIZE)
    digest = _compute_hash(password, salt)
    return salt.hex(), digest.hex()


def verify_password(password, salt, password_hash):
    digest = _compute_hash(password, bytes.fromhex(salt))
    return hmac.compare_digest(digest.hex(), password_hash)


