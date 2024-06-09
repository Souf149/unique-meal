import sqlite3
from time import sleep
from models.connection import Connection
import os
import re

from models.user import hash_password

special_characters = ["~","!","@","#","$","%","&","_","-","+","=","`","|","\\","(",")","{","}","[","]",":",";","'","<",">",",",".","?","/"]

db = Connection()

while True:
    user = None
    username = input("Give your username please: ")
    password = input("Give your password please: ")
    user = db.getUserFromLogin(username, password)
    if user == None:
        print("wrong login")
        continue

    print(f"Logged in with the id: {user['id']}")
    while True:
        print(f"Welcome {user['f_name']}!")


        # Administators
        print("Choose a number to select what you want to do")
        print("1).\tChange my password")
        print("2. Add a new member")
        print("3. Modify a member")
        print("4. Get information of a member")

        # System Administrators")
        print("5. Check list of all users and their roles")
        print("6. Add a new consultant")
        print("7. Update consultant")
        print("8. delete consultant")
        print("9. reset consultant's password (a temporary password)")
        print("10. Backup of the system and restore a backup (members information and users' data)")
        print("11. See the logs file(s) of the system")
        print("12. Delete member's record from the database (note that a consultant cannot delete a record but can only modify or update a member's information)")

        # Super Administrator
        print("13). Add system admin")
        print("14). Edit system admin")
        print("15). Reset admin password (temp one)")


        option = input("Press the corresponding number of the action you want to take or press \"Q\" to log out\n").lower()
        if option == "q":
            print("Logging out")
            os.system('cls')
            break
        elif option == "1":
            while True:
                new_pass = input("What do you want to change your current password into?")
                pass_length = len(new_pass)
                if pass_length < 12 or pass_length > 30:
                    print("Your password must be of length between 12 and 30 please.")
                    continue
                
                # Pass must contain one of the special characters
                if not any(c in special_characters for c in new_pass):
                    print("Please include a special character in your password.")
                    continue
                
                # Pass must only contain A-z 0-9 special characters
                possible_chars_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;\'<>,.?/])$')
                if bool(possible_chars_pattern.match(new_pass)):
                    print("Password can only contain letters, numbers and these characters: ~!@#$%&_\-+=`|\\(){}[\]:;'<>,.?\/\"")
                    continue
                
                # Pass must contain one of each
                pattern = re.compile(
                r'^(?=.*[a-z])'  # At least one lowercase letter
                r'(?=.*[A-Z])'   # At least one uppercase letter
                r'(?=.*\d)'      # At least one digit
                r'(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;\'<>,.?/])'  # At least one special character
                r'[A-Za-z\d~!@#$%&_\-+=`|\\(){}[\]:;\'<>,.?/]+$'  # Only allowed characters
                )

                # one_of_each_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}[\]:;\'<>,.?/])')
                if not bool(pattern.match(new_pass)):
                    print("Make sure the password has at least 1 of each: a lower case letter, an upper case letter, a digit and a special character")
                    continue
                
                user["hashed_pass"] = hash_password(new_pass)
                db.updateUser(user)
                sleep(1)
                print("Password changed succesfully!")
                sleep(1)
                break


        elif option == "2":
            pass

        elif option == "3":
            pass

        elif option == "4":
            pass

        elif option == "5":
            pass

        elif option == "6":
            pass

        elif option == "7":
            pass

        elif option == "8":
            pass

        elif option == "9":
            pass

        elif option == "10":
            pass

        elif option == "11":
            pass

        elif option == "12":
            pass

        elif option == "13":
            pass

        elif option == "14":
            pass

        elif option == "15":
            pass



