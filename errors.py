class PassmanError(Exception):
    """Базовое исключение приложения, от него наследуются все остальные."""


class ValidationError(PassmanError):
    """Бросается, если введённые данные не прошли проверку."""


class MasterExistsError(PassmanError):
    """Бросается при повторном создании мастер-пароля."""


class VaultNotInitializedError(PassmanError):
    """Бросается, если хранилище ещё не создано (не выполнялся --init)."""


class VaultLockedError(PassmanError):
    """Бросается при работе с записями без успешного unlock."""


class EntryExistsError(PassmanError):
    """Бросается, если запись с таким названием уже есть."""


class EntryNotFoundError(PassmanError):
    """Бросается, если записи с таким названием нет."""


class VaultCorruptedError(PassmanError):
    """Бросается, если файл хранилища повреждён или запись не расшифровывается."""
