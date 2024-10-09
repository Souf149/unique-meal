from time import sleep
from imports.connection import Connection
from imports.helper_functions import clear_terminal_with_title, generate_password, hash_password, user_input
from tools.tools import print_user_without_pass
from tools.validators import is_valid
from functionalities import create_account
from imports.validator import User_Info_Validator
import time
from imports.helper_functions import Level, PersonType
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
            print(f"f{victim}")
            if victim is None:
                status = "This ID does not exist, please enter a valid one."
                continue

            print_user_without_pass(victim)
            confirmation = user_input(
                "Is this the user you want to edit? Please input yes or no: "
            )
            if confirmation[0].lower() not in ["y", "yes"]:
                continue

            keys = victim.keys()
            try:
                if user["level"] > victim.get("level", -1):
                    status = ""
                    while True:
                        if (status):
                            print(status)
                        chosen_field = user_input("What field would you like to edit? ")
                        if chosen_field in keys and chosen_field != "hashed_pass":
                            
                            break
                        else:
                            status = "Please choose a valid field."
                            continue
                    
                    new_value = user_input("What would you like this field to become? ")
                    correctvalue = False

                    while True:

                        if chosen_field == "l_name":
                            status = "You've chosen for the value: last name"
                            correctvalue = User_Info_Validator.validate_name(new_value)

                        elif chosen_field == "age" and victim["type"] == PersonType.MEMBER:
                            status = "You've chosen for the value: age"
                            correctvalue = User_Info_Validator.validate_age(new_value)

                        elif chosen_field == "gender" and victim["type"] == PersonType.MEMBER:
                            status = "You've chosen for the value: gender"
                            correctvalue = User_Info_Validator.validate_gender(new_value)

                        elif chosen_field == "weight" and victim["type"] == PersonType.MEMBER:
                            status = "You've chosen for the value: weight"
                            correctvalue = User_Info_Validator.validate_weight(new_value)

                        elif chosen_field == "street" and victim["type"] == PersonType.MEMBER:
                            status = "You've chosen for the value: street"
                            correctvalue = User_Info_Validator.validate_street_name(new_value)

                        elif chosen_field == "house_number" and victim["type"] == PersonType.MEMBER:
                            status = "You've chosen for the value: house number"
                            correctvalue = User_Info_Validator.validate_housenumber(new_value)

                        elif chosen_field == "zip" and victim["type"] == PersonType.MEMBER:
                            status = "You've chosen for the value: zip"
                            correctvalue = User_Info_Validator.validate_zip(new_value)
                            
                        elif chosen_field == "city" and victim["type"] == PersonType.MEMBER:
                            status = "You've chosen for the value: city"
                            correctvalue = create_account.choose_city()

                        elif chosen_field == "email" and victim["type"] == PersonType.MEMBER:
                            status = "You've chosen for the value: email"
                            correctvalue = User_Info_Validator.validate_housenumber(new_value)

                        elif chosen_field == "phone" and victim["type"] == PersonType.MEMBER:
                            status = "You've chosen for the value: phone"
                            correctvalue = User_Info_Validator.validate_phone(new_value)

                        elif chosen_field == "registration_date" and victim["type"] == PersonType.MEMBER:
                            status = "You've chosen for the value: registration_date"
                            
                        elif chosen_field == "id" and victim["type"] == PersonType.MEMBER:
                            correctvalue = User_Info_Validator.validate_id(new_value)
                            status = "You've chosen for the value: ID"
                            
                        elif chosen_field == "f_name":
                            status = "You've chosen for the value: first name"
                            correctvalue = User_Info_Validator.validate_name(new_value)
                        elif chosen_field == "username":
                            status = "You've chosen for the value: username"
                            correctvalue = User_Info_Validator.validate_housenumber(new_value)

                        elif chosen_field == "level" and user["level"] >= Level.SYSTEM_ADMINISTRATOR:
                            while True:
                                print("You've chosen for the value: level")
                                options = " ".join(map( lambda x: f"[{str(x)}] {Level.NAMES[x]}",range(1, user["level"] + 1),))
                                
                                if (new_value == "1" or new_value == "2"):
                                    correctvalue = User_Info_Validator.validate_level(new_value)
                                    break
                                elif (new_value == "3" and user["level"] == Level.SUPER_ADMINISTRATOR):
                                    correctvalue = User_Info_Validator.validate_level(new_value)
                                    break
                                else:
                                    print("Incorrect option! ")
                                    new_value = user_input("Try again! You can only create users of level: {options} and lower!") 
                                    continue
                        else:
                            status = "Incorrect input"
                            time.sleep(2)
                            
                            return 

                        if not correctvalue:
                            status = "That is not a valid input, please try again."
                            time.sleep(2)
                            
                            return  
                        if (correctvalue):
                            victim[chosen_field] = new_value
                            db.updateAcount(victim)
                            db.log(
                                user["username"],
                                "Updated user in database",
                                f"User: {user['username']} has been edited in field: {chosen_field}",
                                False,
                            )
                            status = "Field has been updated!"
                            time.sleep(10)
                            return  # Exit after updating the field
                        else:
                            status = "That is not a valid input, please try again."
                            print("1111133333111")
                            time.sleep(55)
                            
                            return  
            

                else:
                    status = f"You can only change info of users with levels: {user['level']} and lower!"
                    break
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
            time.sleep(2)
            break

        for i, _user in enumerate(users):
            print(
                f"{i + 1}). {_user['type']}\t{_user['id']}\t{_user['username']}"
            )
        userinputid = user_input("Type [0] to go back to the main menu.\nType the ID of the user you want reset the password of.")
        if not (User_Info_Validator.validate_id(userinputid)):
            message = "Incorrect ID, user has not been found!"
            continue
        founduser = db.getAccountFromId(userinputid)
        if (founduser == "0"):
            break

        if not (founduser):
            message = "User has not been found! Try again"
            continue

        if (founduser in users and founduser):
                if (founduser["level"] <= user["level"]):
                    new_pass = generate_password()
                    founduser['hashed_pass'] = hash_password(new_pass)
                    db.updateAcount(founduser)
                    print(f"The new password for this user is {new_pass}")
                    time.sleep(5)
                    break
                options = " ".join(map(lambda x: f"[{str(x)}] {Level.NAMES[x]}",range(1, user["level"] + 1),))
                message = f"You can only reset the passwords of level:{options}"
                continue
        
        message ="Incorrect ID, user has not been found!"
