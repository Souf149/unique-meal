from tools.tools import check_password, user_input
from time import sleep
from models.connection import Connection
from models.user import hash_password
from tools.tools import check_password,clear_terminal_with_title
import os


def change_my_password(db: Connection, user: dict):
    
    while True:
        clear_terminal_with_title("UNIQUE MEAL")
        new_pass = user_input(
            "What do you want to change your current password into?")

        if check_password(new_pass):
            user["hashed_pass"] = hash_password(new_pass)
            db.updateUser(user)
            sleep(1)
            print("Password changed succesfully!")
            sleep(1)
            db.log(user["username"], "Changed password",
                   f"Changed password of user: {user['username']}", False)
            return
