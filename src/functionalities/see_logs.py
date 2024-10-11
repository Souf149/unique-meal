from time import sleep
from imports.connection import Connection
import os

from imports.helper_functions import clear_terminal_with_title


def see_logs(db: Connection):
    clear_terminal_with_title()
    logs = db.get_logs()

    for log in logs:
        if log[-1] == "yes":
            print("[SUSPICIOUS]: ", end="")
        print("%s\t%s\t%s\t%s\t%s" % log)

    input("Please input [0] or something something to go back to the main menu.\n")  # type: ignore
