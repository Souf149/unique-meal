from imports.connection import Connection
from imports.helper_functions import clear_terminal_with_title, user_input
from tools.tools import (
    print_user_without_pass,
)


def list_users(db: Connection, user: dict):
    users = db.getAllUsersAndMembersFromLevelAndLower(user["level"])
    status = ""

    while True:
        clear_terminal_with_title()

        if status:
            print(status)

        print(
            "\nPress [0] to go back to the main menu\nPress [1] to look for a user\nPress [2] to view & choose a user from the list"
        )
        choice = user_input()

        if choice == "1":
            while True:
                clear_terminal_with_title()
                if status:
                    print(status)
                print("LOOKING FOR USER...")
                term = user_input("Input text that we will look for: ")
                users = db.searchForUsersAndMembersByTerm(term)

                if len(users) == 0:
                    print("No users found.\n")
                    choice = user_input(
                        "Press [0] to return to the main menu, or any other key to try again: "
                    )
                    if choice == "0":
                        return
                    else:
                        continue

                clear_terminal_with_title()
                print("These users have been found: ")
                for i, _user in enumerate(users):
                    print(f"{i + 1}). {_user['id']} {_user['username']}")

                option = user_input(
                    "Type the number of the user you want to view information for: "
                )

                while True:
                    if option:
                        if option.isdigit() and 1 <= int(option) <= len(users):
                            try:
                                choose = users[int(option) - 1]
                                clear_terminal_with_title()
                                print_user_without_pass(choose)

                                choice = user_input(
                                    "Press [0] to return to the main menu.\nType any other key to find another user's information: "
                                )

                                if choice == "0":
                                    return
                                else:
                                    status = ""
                                    break

                            except Exception as e:
                                status = f"An error occurred while processing the user data: {e}"
                                break
                        else:
                            status = f"Not a valid option. Press any number from [1] to [{len(users)}]"
                            break
                    else:
                        clear_terminal_with_title("UNIQUE MEMBER")
                        print(
                            "Invalid input! A number is supposed to be given. Please try again."
                        )
                        break

        elif choice == "2":
            while True:
                clear_terminal_with_title()
                if status:
                    print(status)

                print("List of Users:\n")

                if not users:
                    print("No users available.\n")
                    user_input("Press [0] to return to the main menu.")
                    break

                for i, _user in enumerate(users):
                    print(
                        f"{i + 1}). {_user['type']}\t{_user['id']}\t{_user['username']}"
                    )

                option = user_input(
                    "Choose the number of the user you'd like to view information of: "
                )

                if option.isdigit() and 1 <= int(option) <= len(users):
                    chosen_user: dict = users[int(option) - 1]
                    clear_terminal_with_title()
                    print_user_without_pass(chosen_user)

                    choice = user_input(
                        "Press [0] to return to the main menu.\nType any other key to list or find another user's information: "
                    )

                    if choice == "0":
                        return
                    else:
                        status = ""
                        continue
                else:
                    status = "Incorrect list number, please try again."
                    continue
