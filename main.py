import sqlite3
from time import sleep
from functionalities.one import one
from models.connection import Connection
import os
import re

from models.user import hash_password


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
        print("2).\tAdd a new member")
        print("3).\tModify a member")
        print("4).\tGet information of a member")

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


        option = input("Press the corresponding number of the action you want to take or press \"Q\" to log out\n").lower()
        if option == "q":
            print("Logging out")
            os.system('cls')
            break
        elif option == "1":
            one(db, user)

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



