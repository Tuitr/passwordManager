# Password Manager

Консольный менеджер паролей на Python. Вход по мастер-паролю, записи (сервис, логин, пароль) хранятся в `vault.json`, пароли в них зашифрованы.

## Возможности

- создание хранилища и вход по мастер-паролю;
- добавление, список, просмотр и удаление записей;
- просмотр пароля только после повторного ввода мастер-пароля;
- генератор надёжных паролей: строчные и заглавные буквы, цифры, спецсимволы;
- скрытый ввод паролей через `getpass`.

## Запуск

Нужен Python 3.10+.

С [uv](https://docs.astral.sh/uv/):

```bash
uv sync
uv run password_manager.py
```

Без uv:

```bash
pip install -r requirements.txt
python password_manager.py
```

Запускайте из настоящего терминала: в консоли Run в PyCharm скрытый ввод не работает.

## Тесты и проверки

```bash
uv run pytest            # тесты
uv run ruff check .      # линтер
uv run ruff format .     # форматирование
```

Все три проверки запускаются в GitHub Actions при каждом пуше в `main` и в pull request (`.github/workflows/ci.yml`).

## Как устроена безопасность

```
мастер-пароль ─┬─ + salt     → PBKDF2-SHA256 → хеш        → хранится в vault.json, проверяет вход
               └─ + key_salt → PBKDF2-SHA256 → ключ Fernet → только в памяти, шифрует записи
```

- Мастер-пароль не хранится: в файле только хеш PBKDF2-SHA256 (600 000 итераций) со случайной солью.
- Пароли записей зашифрованы Fernet (AES + HMAC) из библиотеки `cryptography`.
- Ключ шифрования выводится из мастер-пароля с отдельной солью и нигде не сохраняется.

## Структура

```
password_manager.py     # точка входа
config.py               # путь к хранилищу и настройки
errors.py               # исключения приложения
models.py               # Entry — запись хранилища
security.py             # хеширование, шифрование, генератор паролей
manager.py              # PasswordManager — работа с хранилищем
ui/
  console.py            # вывод и ввод
  password_input.py     # скрытый ввод пароля
  menu.py               # StartMenu и VaultMenu
tests/                  # pytest
pyproject.toml          # зависимости и настройки ruff и pytest
```