from tools.tools import check_password, user_input
from time import sleep
from models.connection import Connection
from models.user import hash_password
from tools.tools import check_password
from os import listdir
from os.path import isfile, join


def backup(db: Connection):

    files = [f for f in listdir("./backups") if isfile(join("./backups", f))]

    while True:
        for i, file in enumerate(files):
            print(f"{i + 1}).\t {file}")

        choice = user_input(
            "Press the number of the backup you want to restore.\nPress C to create a backup.\nPress Q to quit this screen.")

        if choice.lower() == "c":
            db.make_backup()
            return

        if choice.lower() == "q":
            return

        if choice.isdigit() and int(choice) <= len(files):
            db.restore_backup(files[int(choice) - 1])
