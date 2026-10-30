from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
VAULT_FILE = BASE_DIR / 'vault.json'
HASH_ITERATIONS = 600_000
GENERATED_PASSWORD_LENGTH = 16
MIN_MASTER_LENGTH = 8

