import base64
import hashlib
import hmac
import secrets
import string

from cryptography.fernet import Fernet

from config import HASH_ITERATIONS, GENERATED_PASSWORD_LENGTH

SALT_SIZE = 16

def _compute_hash(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        HASH_ITERATIONS,
    )


def generate_salt():
    return secrets.token_bytes(SALT_SIZE).hex()


def hash_password(password):
    salt = generate_salt()
    digest = _compute_hash(password, bytes.fromhex(salt))
    return salt, digest.hex()


def verify_password(password, salt, password_hash):
    digest = _compute_hash(password, bytes.fromhex(salt))
    return hmac.compare_digest(digest.hex(), password_hash)


def derive_key(password, salt):
    raw = _compute_hash(password, bytes.fromhex(salt))
    return base64.urlsafe_b64encode(raw)


def encrypt(key, text):
    return Fernet(key).encrypt(text.encode("utf-8")).decode("utf-8")


def decrypt(key, token):
    return Fernet(key).decrypt(token.encode("utf-8")).decode("utf-8")

CHAR_GROUPS = (
    string.ascii_lowercase,
    string.ascii_uppercase,
    string.digits,
    string.punctuation,
)


def generate_password(length=GENERATED_PASSWORD_LENGTH):
    if length < len(CHAR_GROUPS):
        raise ValueError(f"Длина пароля должна быть не меньше {len(CHAR_GROUPS)}")

    rng = secrets.SystemRandom()
    all_chars = "".join(CHAR_GROUPS)

    chars = [secrets.choice(group) for group in CHAR_GROUPS]
    chars += [secrets.choice(all_chars) for _ in range(length - len(chars))]
    rng.shuffle(chars)
    return "".join(chars)