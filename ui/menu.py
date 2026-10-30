from errors import PassmanError
from security import generate_password
from ui.console import clear, info, success, error, ask, pause
from ui.password_input import input_password
from config import GENERATED_PASSWORD_LENGTH

class StartMenu:
    def __init__(self, manager):
        self.manager = manager

    def show(self):
        while True:
            clear()
            info("=== Менеджер паролей ===")
            info("1. Создать хранилище")
            info("2. Войти")
            info("3. Сгенерировать пароль")
            info("0. Выход")
            choice = ask("Выберите пункт: ")
            match choice:
                case "1":
                    self._init()
                case "2":
                    self._unlock()
                case "3":
                    self._generate()
                case "0":
                    info("До свидания!")
                    return
                case _:
                    error("Нет такого пункта")
                    pause()

    def _init(self):
        clear()
        info("=== Создание хранилища ===")
        password = input_password("Введите мастер пароль: ")
        password_check = input_password("Введите мастер пароль повторно: ")
        if password != password_check:
            error("Пароли не совпадают")
            pause()
            return
        try:
            self.manager.init_master(password)
            success("Хранилище создано!")
        except PassmanError as e:
            error(str(e))
        pause()


    def _unlock(self):
        clear()
        info("=== Вход ===")
        try:
            master_password = input_password("Введите мастер пароль: ")
            if self.manager.unlock(master_password):
                VaultMenu(self.manager).show()
            else:
                error("Неверный мастер пароль!")
                pause()
        except PassmanError as e:
            error(str(e))
            pause()

    def _generate(self):
        clear()
        info("=== Генератор паролей ===")
        text = ask(f"Длина (Enter — {GENERATED_PASSWORD_LENGTH}): ")
        try:
            if not text:
                length = GENERATED_PASSWORD_LENGTH
            else:
                length = int(text)
            info(f"Пароль: {generate_password(length)}")
        except ValueError:
            error("Введите целое число не меньше 4")
        pause()


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
        password = input_password("Введите пароль (Enter — сгенерировать): ")
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
        master = input_password("Мастер-пароль: ")
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
            success("Запись удалена нахуй!")
        except PassmanError as e:
            error(str(e))
        pause()
