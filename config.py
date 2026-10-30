from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / 'data.json'
VAULT_FILE = BASE_DIR / 'vault.json'
ROLE_USER = "user"
ROLE_ADMIN = "admin"
MIN_LOGIN_LENGTH = 3
MAX_LOGIN_LENGTH = 20
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 30
DEFAULT_ADMIN = {"login": "admin", "password": "admin123"}
HASH_ITERATIONS = 600_000
GENERATED_PASSWORD_LENGTH = 16

