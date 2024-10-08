from imports.helper_functions import hash_password
from tools.tools import check_password, user_input
from time import sleep
from imports.connection import Connection
from tools.tools import check_password, clear_terminal_with_title
from imports.validator import User_Info_Validator
import os


def change_my_password(db: Connection, user: dict):
    status = ""
    while True:
        clear_terminal_with_title("UNIQUE MEAL")
        if status:
            print(status)

        user_choice = user_input(
            "Press [0] to go back to the main menu. Press [1] to change your current password: "
        )

        if user_choice == "0":
            break
        elif user_choice == "1":
            new_pass = user_input(
                "What do you want to change your current password to? "
            )

            # Validate password
            if User_Info_Validator.validate_password(new_pass):
                user["hashed_pass"] = hash_password(new_pass)
                db.updateUser(user)
                print("Password changed successfully!")
                sleep(1)
                db.log(
                    user["username"],
                    "Changed password",
                    f"Changed password of user: [{user['username']}]",
                    False,
                )
                return
            else:
                # Set the status message for incorrect password format
                status = "Incorrect password format!\nPassword must:\n* Be unique\n* Have a length of at least 8 characters\n* Must be no longer than 10 characters\n* Must start with a letter or underscores (_)\n* Can contain letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (.)\n"
        else:
            status = "Wrong option! Choose [0] or [1]."
