from errors import PassmanError
from security import generate_password
from ui.console import clear, info, success, error, ask, pause
from ui.password_input import inputPassword

class VaultMenu:
    def __init__(self, manager):
        self.manager = manager

    def show(self):
        while True:
            clear()
            info("=== Хранилище паролей ===")
            info("1. Добавить запись")
            info("2. Список записей")
            info("3. Показать пароль")
            info("4. Удалить запись")
            info("0. Выход")
            choice = ask("Выберите пункт: ")
            match choice:
                case "1":
                    self._add()
                case "2":
                    self._list()
                case "3":
                    self._get()
                case "4":
                    self._delete()
                case "0":
                    self.manager.lock()
                    info("Хранилище заблокировано")
                    return
                case _:
                    error("Нет такого пункта")
                    pause()

    def _add(self):
        clear()
        info("=== Новая запись ===")
        name = ask("Введите название: ")
        login = ask("Введите логин: ")
        password = inputPassword("Введите пароль (Enter — сгенерировать): ")
        if not password:
            password = generate_password()
            info(f"Сгенерирован пароль: {password}")
        try:
            self.manager.add_entry(name, login, password)
            success("Запись успешно добавлена!")
        except PassmanError as e:
            error(str(e))
        pause()


    def _list(self):
        clear()
        info("=== Список записей ===")
        names = self.manager.list_entries()
        if not names:
            info("Записей пока нет")
        else:
            for i, name in enumerate(names, start=1):
                info(f"{i}. {name}")
        pause()

    def _get(self):
        clear()
        info("=== Просмотр пароля ===")
        name = ask("Введите название: ")
        master = inputPassword("Мастер-пароль: ")
        if not self.manager.unlock(master):
            error("Неверный мастер-пароль")
            pause()
            return
        try:
            login, password = self.manager.get_entry(name)
            info(f"Логин: {login}")
            info(f"Пароль: {password}")
        except PassmanError as e:
            error(str(e))
        pause()
        clear()


    def _delete(self):
        clear()
        info("=== Удаление записи ===")
        name = ask("Введите название: ")
        choice = ask(f"Удалить {name}? (да/нет): ")
        if choice.lower() != "да":
            info("Удаление отменено")
            pause()
            return
        try:
            self.manager.delete_entry(name)
            success("Запись успешно удалена!")
        except PassmanError as e:
            error(str(e))
        pause()
