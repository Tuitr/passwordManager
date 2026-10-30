from manager import PasswordManager
from ui.menu import StartMenu


def main():
    manager = PasswordManager()
    try:
        StartMenu(manager).show()
    except KeyboardInterrupt:
        print("\nПрограмма завершена")


if __name__ == "__main__":
    main()