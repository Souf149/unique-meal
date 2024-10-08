import traceback
from time import sleep

from imports.helper_functions import (
    Level,
    PersonType,
    clear_terminal_with_title,
    user_input,
)
from imports.connection import Connection
from functionalities import backup, change_password, edit_user, list_users, see_logs
from imports import create_user

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
        clear_terminal_with_title()
        while True:
            clear_terminal_with_title()

            print(f"Welcome {user['username']}!")
            print(f"Level: {user['level']}!")

            # Display options based on user level
            if user["type"] == PersonType.MEMBER:  # Member
                print("As a Member, you have no actions available.")
                print('Press "Q" to log out.')

            elif user["level"] == Level.CONSULTANT:  # Consultant
                print("Choose a number to select what you want to do:")
                print("1).\tChange my password")
                print("2).\tAdd a new member")
                print("3).\tModify/update member information")
                print("4).\tSearch/retrieve member information")
                print('Press "Q" to log out.')

            elif user["level"] in [
                Level.SYSTEM_ADMINISTRATORS,
                Level.SUPER_ADMINISTRATOR,
            ]:  # Admin or Super Admin
                print("Choose a number to select what you want to do:")
                print("1).\tChange my password")
                print("2).\tCheck list of users and their roles")
                print("3).\tDefine and add a new consultant")
                print("4).\tModify/update an existing consultant's account")
                print("5).\tDelete an existing consultant's account")
                print("6).\tReset an existing consultant's password")
                print("7).\tAdd a new member")
                print("8).\tModify/update member information")
                print("9).\tSearch/retrieve member information")
                print("10).\tMake/Delete a backup of the system")
                print("11).\tSee logs")
                print("12).\tDefine and add a new admin")  # Admin-specific
                print(
                    "13).\tModify/update an existing admin's account"
                )  # Admin-specific
                print("14).\tDelete an existing admin's account")  # Admin-specific
                print("15).\tReset an existing admin's password")  # Admin-specific
                print('Press "Q" to log out.')

            option = user_input('Select an action or press "Q" to log out: ').lower()

            if option == "q":
                print("Logging out")
                clear_terminal_with_title()  # Clear the screen on logout
                break

            # Handle actions based on user level
            if user["level"] == Level.CONSULTANT:  # Consultant
                if option == "1":
                    change_password.change_my_password(db, user)
                elif option == "2":
                    create_user.create_new_member(db, user)
                elif option == "3":
                    edit_user.edit_user(db, user)
                elif option == "4":
                    list_users.list_users(db, user)
                else:
                    print("Invalid option. Please try again.")
                    sleep(2)  # Small delay before clearing
                    clear_terminal_with_title()  # Clear after an invalid option
                    continue

            elif user["level"] in [
                Level.SYSTEM_ADMINISTRATORS,
                Level.SUPER_ADMINISTRATOR,
            ]:  # Admin or Super Admin
                if option == "1":
                    change_password.change_my_password(db, user)
                elif option == "2":
                    list_users.list_users(db, user)  # Clean gemaakt
                elif option == "3":
                    create_user.create_new_member(db, user)  # Create consultant
                elif option == "4":
                    edit_user.edit_user(db, user)  # Modify consultant
                elif option == "5":
                    edit_user.edit_user(db, user)  # Delete consultant
                elif option == "6":
                    reset_password.reset_consultant_password(
                        db
                    )  # Reset consultant's password
                elif option == "7":
                    create_user.create_new_member(db, user)  # Add new member
                elif option == "8":
                    edit_user.edit_user(db, user)  # Modify member
                elif option == "9":
                    list_users.list_users(db, user)  # Search/retrieve member info
                elif option == "10":
                    backup.backup(db)  # Backup system
                elif option == "11":
                    see_logs.see_logs(db)  # View logs
                elif (
                    option == "12" and user["level"] == 4
                ):  # Only Super Admin can add a new admin
                    create_user.create_new_member(db, user)
                elif option == "13" and user["level"] == 4:  # Admin-specific
                    edit_user.edit_user(db, user)
                elif option == "14" and user["level"] == 4:  # Admin-specific
                    edit_user.edit_user(db, user)
                elif option == "15" and user["level"] == 4:  # Admin-specific
                    reset_password.reset_admin_password(db)  # MOET NOG KOMEN
                else:
                    print("Invalid option. Please try again.")
                    sleep(2)  # Small delay before clearing
                    clear_terminal_with_title()  # Clear after an invalid option
                    continue

            elif user["level"] == 1:  # Member
                print("Members cannot perform any actions in this system.")

            db.db.commit()

except KeyboardInterrupt:
    db.close()
    print("Bye bye :)")
except BaseException:
    if DEBUG:
        print(traceback.format_exc())
    db.close()
