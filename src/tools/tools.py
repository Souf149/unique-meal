from builtins import input
import re
import os
import pyfiglet


def check_password(password: str) -> bool:
    special_characters = [
        "~",
        "!",
        "@",
        "#",
        "$",
        "%",
        "&",
        "_",
        "-",
        "+",
        "=",
        "`",
        "|",
        "\\",
        "(",
        ")",
        "{",
        "}",
        "[",
        "]",
        ":",
        ";",
        "'",
        "<",
        ">",
        ",",
        ".",
        "?",
        "/",
    ]
    pass_length = len(password)
    if pass_length < 12 or pass_length > 30:
        print("Your password must be of length between 12 and 30 please.")
        return False

    # Pass must contain one of the special characters
    if not any(c in special_characters for c in password):
        print("Please include a special character in your password.")
        return False

    # Pass must only contain A-z 0-9 special characters
    possible_chars_pattern = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;\'<>,.?/])$"
    )
    if bool(possible_chars_pattern.match(password)):
        print(
            "Password can only contain letters, numbers and these characters: ~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?\/\""
        )
        return False

    # Pass must contain one of each
    one_of_each_pattern = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;\'<>,.?/])[A-Za-z\d~!@#$%&_\-+=`|\\(){}[\]:;\'<>,.?/]+$"
    )
    if not bool(one_of_each_pattern.match(password)):
        print(
            "Make sure the password has at least 1 of each: a lower case letter, an upper case letter, a digit and a special character"
        )
        return False

    return True


def print_user_without_pass(user: dict):
    for key, value in user.items():
        if key != "hashed_pass":
            print(f"{key}: {value}")


def validate_number(prompt: str):
    while True:
        try:
            value = float(prompt)  # Change to int() if only integers are allowed
            return True
        except ValueError:
            return False


