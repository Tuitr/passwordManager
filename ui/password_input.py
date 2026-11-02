import getpass


def input_password(prompt):
    return getpass.getpass(prompt)


if __name__ == "__main__":
    password = input_password("Password: ")
    print(password)
