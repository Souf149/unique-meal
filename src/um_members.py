import traceback

from imports.helper_functions import (
    Level,
    clear_terminal_with_title,
    user_input,
)
from imports.connection import Connection
from functionalities.backup import backup
from functionalities.change_password import change_my_password
from functionalities.edit_user import edit_account, reset_account_password
from functionalities.list_users import list_users
from functionalities.see_logs import see_logs
from functionalities.create_account import create_new_member

DEBUG = True

with open("./key.key") as f:
    key = f.read()

clear_terminal_with_title()

db = Connection(key)
login_attempts = 0


try:
    while True:
        user = None
        username = user_input("Give your username please: ")
        password = user_input("Give your password please: ")
        login_attempts += 1
        user = db.getUserFromLogin(username, password)
        clear_terminal_with_title()

        if user is None:
            print("wrong login")
            if login_attempts > 5:
                db.log(
                    "",
                    "Unsuccessful login.",
                    f"username: {username}. Multiple usernames and passwords are tried in a row.",
                    True,
                )
            else:
                db.log("", "Unsuccessful login.", f"username: {username}.", False)
            continue

        # SUCCESFUL LOGIN
        print(f"Logged in with the id: {user['id']}")

        while True:
            clear_terminal_with_title()

            print(f"Welcome {user['f_name']}!")
            print(f"Level: {Level.NAMES[user['level']]}!")

            print("Choose a number to select what you want to do:")
            print("1).\tChange my password")
            print("2).\tAdd a new member")
            print("3).\tModify/delete account information")
            print("4).\tSearch/retrieve account information")

            if user["level"] in [
                Level.SYSTEM_ADMINISTRATOR,
                Level.SUPER_ADMINISTRATOR,
            ]:
                print("5).\tReset an existing account's password")
                print("6).\tMake/Delete a backup of the system")
                print("7).\tSee logs")

            option = user_input('Select an action or press "Q" to log out: ').lower()

            if option == "q":
                print("Logging out")
                clear_terminal_with_title()
                break

            if option == "1":
                change_my_password(db, user)
            if option == "2":
                create_new_member(db, user)
            if option == "3":
                edit_account(db, user)
            if option == "4":
                list_users(db, user)  # TODO: download whole database and manually query

            if user["level"] in [
                Level.SYSTEM_ADMINISTRATOR,
                Level.SUPER_ADMINISTRATOR,
            ]:
                if option == "5":
                    reset_account_password(db, user)
                if option == "6":
                    backup(db)
                if option == "7":
                    see_logs(db)

            db.db.commit()

except KeyboardInterrupt:
    db.close()
    print("Bye bye :)")
except BaseException:
    if DEBUG:
        print(traceback.format_exc())
    db.close()
