import sqlite3
import traceback
from time import sleep
from functionalities.edit_user import edit_user
from functionalities.list_users import list_users
from functionalities.change_password import change_my_password
from functionalities.create_user import create_new_user
from functionalities.see_logs import see_logs
from models.connection import Connection
import os
import re
from tools.tools import check_password, user_input

from models.user import Level, hash_password

with open("./key.key") as f:
    key = f.read()


db = Connection(key)
login_attempts = 0
try:
    while True:
        user = None
        username = user_input("Give your username please: ")
        password = user_input("Give your password please: ")
        login_attempts += 1
        user = db.getUserFromLogin(username, password)
        if user == None:
            print("wrong login")
            if login_attempts > 5:
                db.log("", "Unsuccessful login.", f"username: {username}. Multiple usernames and passwords are tried in a row.", True)
            else:
                db.log("", "Unsuccessful login.", f"username: {username}.", False)
            continue

        print(f"Logged in with the id: {user['id']}")
        while True:
            print(f"Welcome {user['f_name']}!")

            print("Choose a number to select what you want to do")
            print("1).\tChange my password")
            print("2).\tAdd a new user")
            print("3).\tGet information about a member")
            print("4).\tEdit/Delete a member")
            print("5).\tSee logs")

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
                see_logs(db)

            
            db.db.commit()
except:
    db.close()
