import sqlite3
from time import sleep
from functionalities.edit_user import edit_user
from functionalities.list_users import list_users
from functionalities.change_password import change_my_password
from functionalities.create_user import create_new_user
from models.connection import Connection
import os
import re
from tools.tools import check_password, user_input

from models.user import Level, hash_password


db = Connection()

try:
    while True:
        user = None
        username = user_input("Give your username please: ")
        password = user_input("Give your password please: ")
        
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
            print("2).\tAdd a new member")
            print("3).\tGet information about a member")
            print("4).\tEdit/Delete a member")

            # System Administrators")
            print("5).\tCheck list of all users and their roles")
            print("6).\tAdd a new consultant")
            print("7).\tUpdate consultant")
            print("8).\tdelete consultant")
            print("9).\treset consultant's password (a temporary password)")
            print("10).\tBackup of the system and restore a backup (members information and users' data)")
            print("11).\tSee the logs file(s) of the system")
            print("12).\tDelete member's record from the database (note that a consultant cannot delete a record but can only modify or update a member's information)")

            # Super Administrator
            print("13).\tAdd system admin")
            print("14).\tEdit system admin")
            print("15).\tReset admin password (temp one)")

            option = user_input(
                "Press the corresponding number of the action you want to take or press \"Q\" to log out").lower()
            if option == "q":
                print("Logging out")
                os.system('cls')
                break

            elif option == "1":
                change_my_password(db, user)

            elif option == "2":
                create_new_user(db, user, Level.MEMBER)

            elif option == "3":
                list_users(db, user)

            elif option == "4":
                edit_user(db, user)

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
except Exception as e:
    print(e)
    print("Something went wrong, shutting down...")
    db.close()
