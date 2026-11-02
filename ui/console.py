import os


def clear() -> None:
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"  # вернуть обычный цвет


def info(text) -> None:
    print(text)


def success(text) -> None:
    print(f"{GREEN}{text}{RESET}")


def error(text) -> None:
    print(f"{RED}{text}{RESET}")


def ask(prompt):
    return input(prompt).strip()


def pause() -> None:
    input("\nНажмите Enter, чтобы продолжить...")
