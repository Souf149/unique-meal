from datetime import date, datetime
import sqlite3
import time
import zipfile
import os
import shutil
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import cryptography

from .helper_functions import (
    Level,
    PersonType,
    create_member_dict,
    create_member_tuple,
    create_user_dict,
    create_user_tuple,
    generate_id,
    hash_password,
)

FILE_NAME: str = "database.db"


class Connection:
    def __init__(self, private_key, public_key) -> None:
        self.db = sqlite3.connect(FILE_NAME)

        self.private_key = private_key
        self.public_key = public_key

        self.init_user_database_if_needed()
        self.init_member_database_if_needed()
        self.init_logs_if_needed()

    def init_logs_if_needed(self):
        cursor = self.db.cursor()
        create_logs_table_query = """
            CREATE TABLE IF NOT EXISTS logs (
                No INTEGER PRIMARY KEY AUTOINCREMENT,
                Time TEXT NOT NULL,
                Username TEXT NOT NULL,
                Description_of_activity TEXT NOT NULL,
                Additional_Information TEXT,
                Suspicious TEXT NOT NULL
            )
        """

        cursor.execute(create_logs_table_query)
        self.db.commit()

    def init_user_database_if_needed(self) -> None:
        cursor = self.db.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS USERS (
            id TEXT PRIMARY KEY,
            f_name BLOB NOT NULL,
            l_name BLOB NOT NULL,
            level INTEGER NOT NULL,
            username BLOB NOT NULL UNIQUE,
            registration_date DATE NOT NULL,
            hashed_pass BLOB NOT NULL
        )
        """)

        starter_data = [
            create_user_tuple(
                "2400000000",
                "teacher",
                "INF",
                Level.SUPER_ADMINISTRATOR,
                "super_admin",
                datetime.now(),
                hash_password("Admin_123?"),
            ),
            create_user_tuple(
                "2400000001",
                "rdc",
                "def",
                Level.SYSTEM_ADMINISTRATOR,
                "cecilus",
                datetime.now(),
                hash_password("Lol123."),
            ),
            create_user_tuple(
                "2400000002",
                "teacher",
                "INF",
                Level.SYSTEM_ADMINISTRATOR,
                "souf149",
                datetime.now(),
                hash_password("a"),
            ),
            create_user_tuple(
                "2400000003",
                "random",
                "random2",
                Level.CONSULTANT,
                "consult",
                datetime.now(),
                hash_password("Lol123."),
            ),
        ]

        cursor.execute("SELECT COUNT(*) FROM USERS")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                """
                INSERT INTO USERS (id, f_name, l_name, level, username, registration_date, hashed_pass)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                self._encrypt_multiple_user_tuples(starter_data),
            )
            print("Dummy data inserted into USERS table.")
        else:
            print("USERS table already contains data. No new data inserted.")

        self.db.commit()

    def init_member_database_if_needed(self) -> None:
        cursor = self.db.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS MEMBERS (
            id TEXT PRIMARY KEY,
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
            create_member_tuple(
                "2400000000",
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
                hash_password("Lol123."),
            ),
            create_member_tuple(
                generate_id(),
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
            create_member_tuple(
                generate_id(),
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
            create_member_tuple(
                generate_id(),
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

        cursor.execute("SELECT COUNT(*) FROM MEMBERS")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                """
            INSERT INTO MEMBERS (id, f_name, l_name, age, gender, weight, street, house_number, zip, city, email, phone, registration_date, username, hashed_pass)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                starter_data,
            )
            print("Dummy data inserted into MEMBERS table.")
        else:
            print("MEMBERS table already contains data. No new data inserted.")

        self.db.commit()

    def log(self, username: str, desc: str, add_info: str, suspicious: str):
        insert_log_query = """
            INSERT INTO logs (Time, Username, Description_of_activity, Additional_Information, Suspicious)
            VALUES (?, ?, ?, ?, ?)
        """

        cursor = self.db.cursor()
        cursor.execute(
            insert_log_query,
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                username,
                desc,
                add_info,
                1 if suspicious else 0,
            ),
        )
        self.db.commit()

    def getUserFromLogin(self, username: str, password: str) -> dict | None:
        hashed = hash_password(password)

        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM USERS")

        users = cursor.fetchall()

        for enc_u in users:
            user = self._user_dict_from_tuple(self._decrypt_user_tuple(enc_u))
            if user["username"] == username and bytes(user["hashed_pass"]) == bytes(
                hashed
            ):
                return user
        return None

    def getAccountFromId(self, id: str) -> dict | None:
        cursor = self.db.cursor()

        # Query to get the user by their ID
        get_user_query = """
            SELECT *
            FROM USERS
            WHERE id = ?
        """

        cursor.execute(get_user_query, (id,))
        user = cursor.fetchone()
        if user is None:
            # Query to get the user by their ID
            get_member_query = """
                SELECT *
                FROM MEMBERS
                WHERE id = ?
            """

            cursor.execute(get_member_query, (id,))

            member = cursor.fetchone()
            if member is None:
                return None

            return self._member_dict_from_tuple(member)
        return self._user_dict_from_tuple(self._decrypt_user_tuple(user))

    def updateAcount(self, updatedAcount: dict):
        cursor = self.db.cursor()

        values = tuple(
            updatedAcount[key]
            for key in updatedAcount.keys()
            if key not in ["id", "type"]
        )
        values += (updatedAcount["id"],)
        set_clause = ", ".join(
            [f"{key} = ?" for key in updatedAcount.keys() if key not in ["type"]]
        )

        table = "USERS" if updatedAcount["type"] == PersonType.USER else "MEMBERS"

        update_query = f"""
            UPDATE {table}
            SET {set_clause}
            WHERE id = ?
        """
        print(update_query)
        print(updatedAcount)
        del updatedAcount["type"]
        if table == "USERS":
            encrypted_user = self._encrypt_user_tuple(
                create_user_tuple(**updatedAcount)
            )
            cursor.execute(update_query, (encrypted_user + (encrypted_user[0],)))
        else:
            cursor.execute(update_query, tuple(values))

        self.db.commit()
        # self, id: str, chosen_field: str, data, is_user: bool data = gewenste veld , is_user = user of niet

    def updateFieldOfAccount(self, idx: str, chosen_field: str, data, is_user: bool):
        cursor = self.db.cursor()
        # self, id: str, chosen_field: str, data, is_user: bool data = gewenste veld , is_user = user of niet
        if chosen_field in ["f_name", "l_name", "username"] and is_user:
            database_value = self._encrypt(data)
        else:
            database_value = data

        table = "USERS" if is_user else "MEMBERS"

        update_query = f"""
            UPDATE {table}
            SET {chosen_field} = ?
            WHERE id = ?
        """

        print(update_query)
        print(f"Updating {table}: {chosen_field} = {database_value}, id = {idx}")

        cursor.execute(update_query, (database_value, idx))

        self.db.commit()

    def usernameExist(self, username: str):
        # Connect to SQLite database
        cursor = self.db.cursor()

        # Query to check if username already exists
        check_username_query = """
            SELECT COUNT(*)
            FROM USERS
            WHERE username = ?
        """

        cursor.execute(check_username_query, (username,))
        result = cursor.fetchone()

        return result[0] > 0

    def addUser(self, user: tuple):
        cursor = self.db.cursor()

        potential_user = self.getAccountFromId(user[0])
        while potential_user:
            list_user = list(user)
            list_user[0] = generate_id()
            user = tuple(list_user)
            potential_user = self.getAccountFromId(user[0])

        cursor.execute(
            """
                INSERT INTO USERS (id, f_name, l_name, level, username, registration_date, hashed_pass)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            self._encrypt_user_tuple(user),
        )
        self.db.commit()

    def addMember(self, member: tuple):
        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO MEMBERS (id, f_name, l_name, age, gender, weight, street, house_number, zip, city, email, phone, registration_date, username, hashed_pass)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            member,
        )
        self.db.commit()

    def getAllUsersAndMembersFromLevelAndLower(self, level: int) -> list[dict]:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM USERS")
        raw_users = cursor.fetchall()
        users = self._user_dicts_from_tuples(
            self._decrypt_multiple_user_tuples(raw_users)
        )

        cursor.execute("SELECT * FROM MEMBERS")
        raw_members = cursor.fetchall()
        members = self._member_dicts_from_tuples(raw_members)

        return list(filter(lambda x: x["level"] <= level, users)) + members

    def searchForUsersAndMembersByTerm(self, term: str) -> list[dict]:
        cursor = self.db.cursor()
        search_query = """
            SELECT *
            FROM MEMBERS
            WHERE
                f_name LIKE ? OR
                l_name LIKE ? OR
                gender LIKE ? OR
                street LIKE ? OR
                house_number LIKE ? OR
                zip LIKE ? OR
                city LIKE ? OR
                email LIKE ? OR
                phone LIKE ? OR
                username LIKE ?
        """
        cursor.execute(
            search_query,
            (term, term, term, term, term, term, term, term, term, term),
        )
        matching_members = cursor.fetchall()

        search_query = """
            SELECT *
            FROM USERS
            WHERE
                id LIKE ? OR
                username LIKE ?
        """
        cursor.execute(
            search_query,
            (term, term),
        )
        matching_users = cursor.fetchall()

        return self._user_dicts_from_tuples(
            matching_users
        ) + self._member_dicts_from_tuples(matching_members)

    def delete_user(self, id):
        cursor = self.db.cursor()
        delete_user_query = """
            DELETE FROM USERS
            WHERE id = ?
        """

        cursor.execute(delete_user_query, (id,))

        self.db.commit()

    def get_logs(self) -> list[tuple]:
        cursor = self.db.cursor()

        cursor.execute("""
            SELECT *
            FROM logs
        """)

        return cursor.fetchall()

    def _user_dict_from_tuple(self, tuple: tuple) -> dict:
        return create_user_dict(tuple)

    def _user_dicts_from_tuples(self, tuples: list[tuple]) -> list[dict]:
        return list(map(create_user_dict, tuples))

    def _member_dict_from_tuple(self, tuple: tuple) -> dict:
        return create_member_dict(tuple)

    def _member_dicts_from_tuples(self, tuples: list[tuple]) -> list[dict]:
        return list(map(create_member_dict, tuples))

    def _encrypt(self, data: str) -> bytes:
        print(f"ENCRYPTING: {str(data.encode())}")
        x = self.public_key.encrypt(
            data.encode(),
            padding.PKCS1v15(),
        )
        print(f"ENCRYPTED: {x}")

        return x

    def _decrypt(self, data: bytes) -> str:
        return self.private_key.decrypt(
            data,
            padding.PKCS1v15(),
        ).decode()

    def _encrypt_multiple_user_tuples(self, tuples: list[tuple]) -> list[tuple]:
        return [self._encrypt_user_tuple(tup) for tup in tuples]

    def _encrypt_user_tuple(self, tup: tuple) -> tuple:
        return (
            tup[0],
            self._encrypt(tup[1]),
            self._encrypt(tup[2]),
            tup[3],
            self._encrypt(tup[4]),
            tup[5],
            tup[6],
        )

    def _decrypt_multiple_user_tuples(self, tuples: list[tuple]) -> list[tuple]:
        return [self._decrypt_user_tuple(tup) for tup in tuples]

    def _decrypt_user_tuple(self, tup: tuple) -> tuple:
        return (
            tup[0],
            self._decrypt(tup[1]),
            self._decrypt(tup[2]),
            tup[3],
            self._decrypt(tup[4]),
            tup[5],
            tup[6],
        )

    def close(self):
        self.db.commit()
        self.db.close()

        print("Safely exited!")

    def make_backup(self):
        with open(FILE_NAME, "rb") as db_file:
            decrypted_data = db_file.read()

        inpath = f"./_temp/{FILE_NAME}"  # uniquemeal.db
        inpath_check = f"./_temp"
        outpath = "./backups/" + datetime.now().strftime("%Y-%m-%d.%H-%M-%S") + ".zip"

        if not os.path.exists(inpath_check):
            os.makedirs(inpath_check)
            print("Temporary directory created.")
            return

        with open(inpath, "wb") as file:
            file.write(decrypted_data)

        with zipfile.ZipFile(outpath, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(inpath, os.path.basename(inpath))

    def restore_backup(self, file_name):
        BACKUP_FOLDER = "./backups"
        CURRENT_DB_FOLDER = "./"
        DATABASE_FILE = "database.db"
        backup_file = file_name

        try:
            backup_path = os.path.join(BACKUP_FOLDER, backup_file)

            if not os.path.exists(backup_path):
                print("Backup file not found.")
                return

            temp_dir = "./_temprestore"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
                print("Temporary directory created.")
                time.sleep(2)
            with zipfile.ZipFile(backup_path, "r") as zipf:
                print(backup_path)
                zipf.extract(DATABASE_FILE, temp_dir)
            print("dfdsgfdggd")

            extracted_db_path = os.path.join(temp_dir, DATABASE_FILE)
            print(f"Extracted to: {extracted_db_path}")
            print("ywetgweed")

            current_db_path = os.path.join(CURRENT_DB_FOLDER, DATABASE_FILE)

            backup_current_db = os.path.join(
                CURRENT_DB_FOLDER, "backup_" + DATABASE_FILE
            )
            shutil.copy2(current_db_path, backup_current_db)
            print("FDFDFFFDFFD")

            print(f"Backup of the current database created at: {backup_current_db}")

            shutil.copy2(extracted_db_path, current_db_path)
            print(f"Database replaced successfully with {extracted_db_path}")

        except Exception as e:
            print(f"An error occurred: {e}")
