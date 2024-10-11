from time import sleep
from imports.connection import Connection
from imports.helper_functions import PersonType, clear_terminal_with_title, filter_accounts, generate_password, hash_password, user_input
from imports.validator import User_Info_Validator
from tools.tools import print_user_without_pass
from tools.validators import is_valid


def edit_account(db: Connection, user: dict):
    status = ""
    while True:
        clear_terminal_with_title()
        if status:
            print(status)

        print(
            "Press [0] to go back to the main menu\nPress [1] to go to the option ID of the user you'd like to edit\nPress [2] to delete a user"
        )
        choice = user_input("Please choose an option: ")

        if choice == "1":
            clear_terminal_with_title()
            user_id = user_input(
                "Please input the ID of the user you'd like to edit (or press [0] to quit): "
            )
            if user_id.lower() == "0":
                return

            victim = db.getAccountFromId(user_id)
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
                if user["level"] > victim.get("level", -1):
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
                            db.updateAcount(victim) # SOUF REJEL
                            db.log(
                                user["username"],
                                "Updated user in database",
                                f"User: {user['username']} has been edited in field: {chosen_field}",
                                "no",
                            )
                            status = "Field has been updated!"
                            sleep(1)
                            break
                        status = "That is not a valid input, please try again."
                else:
                    status = f"You can only change info of users with levels: {user['level']} and lower!"
                    continue
            except KeyError as e:
                status = f"Key error occurred: {e}. Please ensure that 'level' exists in the user dictionary."
            except Exception as e:
                status = f"An unexpected error occurred: {e}"

        if choice == "2":
            clear_terminal_with_title()
            print("We are going to DELETE a user")
            user_id = user_input("Please enter the ID of the user you want to delete: ")
            victim = db.getAccountFromId(user_id)

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
                        "no",
                    )
                    continue
                else:
                    status = "You do not have permission to delete this user."
            except KeyError as e:
                status = f"Key error occurred: {e}. Please ensure that 'level' exists in the user dictionary."
            except Exception as e:
                status = f"An unexpected error occurred: {e}"
            continue

        if choice == "0":
            return

        else:
            status = "Invalid option. Please choose option [0], [1], or [2]."


def reset_account_password(db: Connection, user: dict):
    message = ""
    while True:
        clear_terminal_with_title()
        if (message):
            print(message)
        users = db.getAllUsersAndMembersFromLevelAndLower(user["level"])
        if not users:
            print("No users available.\n")
            sleep(2)
            break

        for i, _user in enumerate(users):
            print(
                f"{i + 1}). {_user['type']}\t{_user['id']}\t{_user['username']}"
            )
        choice = user_input("Type [0] to go back to the main menu.\nType [1] to choose search for the user you want reset the password of.")
        if (choice == "0"):
            return
        elif (choice == "1"):
            break
        else:
            message = "Incorrect option! Choose 1 or 2"
            continue
    while True:
        if (message):
            print(message)
        userinputid = user_input("What is the id of the user you'd like to reset the password of?")
        if (   userinputid.isdigit() and len(userinputid) == 10):  
            print("DSSDDS")
            #founduser =  filter_accounts(users, userinputid)
            founduser = db.getAccountFromId(userinputid)
            print(founduser)
            sleep(2)
            #booltest = User_Info_Validator.validate_id(userinputid)
            if ( founduser ):
                print("FSFDSFDF")
                #sleep(100)
                if ( founduser['type'] == PersonType.MEMBER ):
                    new_pass = generate_password()
                    new_pass_placeholder = generate_password()
                    #founduser['hashed_pass'] = hash_password(new_pass)
                    new_pass = hash_password(new_pass)
                    if ( user["type"] == PersonType.MEMBER):
                        is_user = False
                    else:
                        is_user = True
                    db.updateFieldOfAccount(userinputid, "hashed_pass", new_pass , is_user) 
                    print(f"The new password for this user is {new_pass_placeholder}")
                    sleep(10)
                    break
                elif (founduser["level"] <= user["level"]):
                    new_pass = generate_password()
                    founduser['hashed_pass'] = hash_password(new_pass)
                    db.updateAcount(founduser)
                    print(f"The new password for this user is {new_pass}")
                    sleep(5)
                    break
                else:
                    options = " ".join(map(lambda x: f"[{str(x)}] {Level.NAMES[x]}",range(1, user["level"] + 1),))
                    message = f"You can only reset the passwords of level:{options}"
                    continue
            else:
                message = "User has not been found! Wrong ID" 
                continue     
        else:
            message = "Incorrect ID! See the list"
            continue