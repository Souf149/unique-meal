import os
from time import sleep
from models.connection import Connection
from tools.tools import print_user_without_pass, user_input, clear_terminal_with_title
from tools.validators import is_valid


def edit_user(db: Connection, user: dict):
    status = ""  # Initialize status message
    while True:
        clear_terminal_with_title("UNIQUE MEAL")  # Title for the main menu
        if status:
            print(status)

        print(
            "Press [0] to go back to the main menu\nPress [1] to go to the option ID of the user you'd like to edit\nPress [2] to delete a user"
        )
        choice = user_input("Please choose an option: ")

        if choice == "2":
            clear_terminal_with_title("UNIQUE MEAL")  # Title for delete user option
            print("We are going to DELETE a user")
            user_id = user_input("Please enter the ID of the user you want to delete: ")
            victim = db.getUserFromId(user_id)

            if victim is None:
                status = "User not found..."
                continue

            try:
                if user["level"] > victim["level"]:
                    db.delete_user(user_id)
                    status = "User has been deleted."
                    db.log(
                        user["username"],
                        "User has been deleted",
                        f"User was of level: {victim['level']}",
                        False,
                    )
                    continue
                else:
                    status = "You do not have permission to delete this user."
            except KeyError as e:
                status = f"Key error occurred: {e}. Please ensure that 'level' exists in the user dictionary."
            except Exception as e:
                status = f"An unexpected error occurred: {e}"
            continue

        if choice == "1":
            clear_terminal_with_title("UNIQUE MEAL")  # Title for edit user option
            user_id = user_input(
                "Please input the ID of the user you'd like to edit (or press [0] to quit): "
            )
            if user_id.lower() == "0":
                return

            victim = db.getUserFromId(user_id)
            if victim is None:
                status = "This ID does not exist, please enter a valid one."
                continue

            print_user_without_pass(victim)
            confirmation = user_input(
                "Is this the user you want to edit? Please input yes or no: "
            )
            if confirmation[0].lower() != "y":
                continue

            keys = victim.keys()
            try:
                if user["level"] > victim["level"]:
                    while True:
                        chosen_field = user_input("What field would you like to edit? ")
                        if chosen_field in keys and chosen_field != "hashed_pass":
                            break
                        status = "Please choose a valid field."

                    while True:
                        new_value = user_input(
                            "What would you like this field to become? "
                        )
                        if is_valid(chosen_field, new_value):
                            victim[chosen_field] = new_value
                            db.updateUser(victim)
                            db.log(
                                user["username"],
                                "Updated user in database",
                                f"User: {user['username']} has been edited in field: {chosen_field}",
                                False,
                            )
                            status = "Field has been updated!"
                            sleep(1)
                            break
                        status = "That is not a valid input, please try again."
                else:
                    status = f"You can only change info of users with levels: {user['level']} and lower!"
            except KeyError as e:
                status = f"Key error occurred: {e}. Please ensure that 'level' exists in the user dictionary."
            except Exception as e:
                status = f"An unexpected error occurred: {e}"

        if choice == "0":
            return

        else:
            status = "Invalid option. Please choose option [0], [1], or [2]."
