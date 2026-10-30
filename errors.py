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


class UserExistsError(PassmanError):
    """Бросается, если логин уже занят: при регистрации или смене логина."""


class UserNotFoundError(PassmanError):
    """Бросается, если пользователь с таким логином не найден."""


class WrongCredentialsError(PassmanError):
    """Бросается при неверном логине или пароле, а также при неверном старом пароле."""


class NotAdminError(PassmanError):
    """Бросается, если пользователь без роли admin пытается войти в панель администратора."""


class CannotDeleteError(PassmanError):
    """Бросается, если администратор пытается удалить себя или другого администратора."""

