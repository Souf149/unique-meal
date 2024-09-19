from datetime import date
from enum import IntEnum
import sqlite3
import traceback
from time import sleep
from src import helper_functions as hf
import os
import re
from Crypto.Hash import SHA256
from cryptography.fernet import Fernet
from pathlib import Path


class Level(IntEnum):
    SUPER_ADMINISTRATOR = 4
    SYSTEM_ADMINISTRATORS = 3
    CONSULTANT = 2
    MEMBER = 1


def hash_password(password: str) -> bytes:
    hash_object = SHA256.new(data=(password).encode())
    return hash_object.digest()


def user_input(prompt: str = "") -> str:
    res = ""
    while res == "":
        res = input(prompt + "\n")
    return str(res)


class Connection:
    def __init__(self, key: str) -> None:
        self.fernet = Fernet(key)
        my_file = Path("./users.encrypted")
        if my_file.is_file():
            with open("./users.encrypted", "rb") as file:
                encrypted_data = file.read()

                decrypted_data = self.fernet.decrypt(encrypted_data)

                with open("users.db", "wb") as db_file:
                    db_file.write(decrypted_data)

        self.db = sqlite3.connect("users.db")

        self.init_database_if_needed()
        self.init_logs_if_needed()

    def init_database_if_needed(self) -> None:
        cursor = self.db.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS USERS (
            id TEXT PRIMARY KEY,
            level INTEGER NOT NULL,
            f_name TEXT NOT NULL,
            l_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            weight REAL NOT NULL,
            street TEXT NOT NULL,
            house_number TEXT NOT NULL,
            zip TEXT NOT NULL,
            city TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            registration_date DATE NOT NULL,
            username TEXT NOT NULL UNIQUE,
            hashed_pass TEXT NOT NULL
        )
        """)

        starter_data = [
            hf.create_user_tuple(
                "2400000000",
                Level.SUPER_ADMINISTRATOR,
                "teacher",
                "INF",
                31,
                "m",
                70.2,
                "wijnhaven",
                "207",
                "4294",
                "Rotterdam",
                "cmi@hr.nl",
                "+31-6-12345678",
                date(2023, 3, 1),
                "teacher23",
                hash_password("Admin_123?"),
            ),
            hf.create_user_tuple(
                hf.generate_id(),
                Level.SYSTEM_ADMINISTRATORS,
                "Soufyan",
                "Abdell",
                25,
                "m",
                257,
                "otherstreet",
                "134",
                "2342",
                "Dordrecht",
                "0963595@hr.nl",
                "+31-6-21424244",
                date(2023, 3, 3),
                "souf149",
                hash_password("a"),
            ),
            create_user_tuple(
                generate_id(),
                Level.CONSULTANT,
                "Reajel",
                "Cic",
                26,
                "m",
                50,
                "boringstreet",
                "24",
                "2556",
                "Pap",
                "1535233@hr.nl",
                "+31-6-11141111",
                date(2024, 6, 7),
                "captainxx",
                hash_password("a"),
            ),
            create_user_tuple(
                generate_id(),
                Level.MEMBER,
                "Cynthia",
                "Amel",
                19,
                "f",
                52,
                "lijnbaan",
                "2",
                "1111",
                "Pap",
                "1534433@hr.nl",
                "+31-6-22141111",
                date(2024, 7, 6),
                "flower",
                hash_password("ab"),
            ),
        ]

        cursor.execute("SELECT COUNT(*) FROM USERS")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                """
            INSERT INTO USERS (id, level, f_name, l_name, age, gender, weight, street, house_number, zip, city, email, phone, registration_date, username, hashed_pass)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                starter_data,
            )
            print("Dummy data inserted into USERS table.")
        else:
            print("USERS table already contains data. No new data inserted.")

        self.db.commit()

    def init_logs_if_needed(self):
        cursor = self.db.cursor()
        create_logs_table_query = """
            CREATE TABLE IF NOT EXISTS logs (
                No INTEGER PRIMARY KEY AUTOINCREMENT,
                Time TEXT NOT NULL,
                Username TEXT NOT NULL,
                Description_of_activity TEXT NOT NULL,
                Additional_Information TEXT,
                Suspicious BOOLEAN NOT NULL CHECK (Suspicious IN (0, 1))
            )
        """

        cursor.execute(create_logs_table_query)
        self.db.commit()

    def getUserFromLogin(self, username: str, password: str) -> dict | None:
        raise NotImplementedError("")
        if username:
            return {}
        else:
            return None

    def log(self, username: str, desc: str, add_info: str, suspicious: bool) -> None:
        print(f"{username}, {desc}, {add_info}, {suspicious}")
        raise NotImplementedError("")


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
        if user is None:
            print("wrong login")
            if login_attempts > 5:
                db.log(
                    "",
                    "Unsuccessful login.",
                    f"username: {username}. Multiple usernames and passwords are tried in a row.",
                    True,
                )
            else:
                db.log("", "Unsuccessful login.", f"username: {username}.", False)
            continue

        # SUCCESFUL LOGIN
        print(f"Logged in with the id: {user['id']}")
        while True:
            print(f"Welcome {user['f_name']}!")

            print("Choose a number to select what you want to do")
            print("1).\tChange my password")
            print("2).\tAdd a new user")
            print("3).\tGet information about a member")
            print("4).\tEdit/Delete a member")
            print("5).\tSee logs")
            print("6).\tCreate/Load backups")

            option = user_input(
                'Press the corresponding number of the action you want to take or press "Q" to log out'
            ).lower()
            if option == "q":
                print("Logging out")
                os.system("cls")
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

            elif option == "6":
                backup(db)

            db.db.commit()
except Exception:
    print(traceback.format_exc())
    db.close()
