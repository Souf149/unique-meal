from time import sleep
from imports.connection import Connection
from tools.tools import user_input, clear_terminal_with_title
import os


def see_logs(db: Connection):
    clear_terminal_with_title()
    logs = db.get_logs()

    print("No.\tTime\tLogged in user\tDescription\tAdditional information\tSuspicous")
    for log in logs:
        print("%s\t%s\t%s\t%s\t%s\t%s" % log)

    input("Please input [0] or something something to go back to the main menu.\n")  # type: ignore
