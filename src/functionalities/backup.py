from tools.tools import check_password, user_input, clear_terminal_with_title
from time import sleep
from imports.connection import Connection
from os import listdir
from os.path import isfile, join
import os


def backup(db: Connection):
    abspath = os.path.abspath("./backups")
    files = [f for f in listdir(abspath) if isfile(join(abspath, f))]
    while True:
        clear_terminal_with_title()
        print("Available backups:")
        for i, file in enumerate(files):
            print(f"{i + 1}).\t {file}")

        print("\nOptions:")
        print(
            "Press [0] to quit.\nPress [1] choose a backup to restore.\nPress [2] to create a backup."
        )

        choice = user_input("Please enter your choice: ")

        if choice == "1":
            backup_choice = user_input(
                "Enter the number of the backup you want to restore (or press 0 to go back): "
            )
            if backup_choice.isdigit() and int(backup_choice) <= len(files):
                db.restore_backup(files[int(backup_choice) - 1])
                print(
                    f"Backup '{files[int(backup_choice) - 1]}' has been restored successfully."
                )
            elif backup_choice == "0":
                continue
            else:
                print("Invalid selection. Please try again.")

        elif choice == "2":
            db.make_backup()
            files = [f for f in listdir(abspath) if isfile(join(abspath, f))]
            print("A new backup has been created successfully.")

        elif choice == "0":
            print("Exiting the backup menu.")
            return

        else:
            print("Invalid choice. Please try again.")
