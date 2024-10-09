from datetime import date, datetime
import sqlite3
import zipfile
import os
from cryptography.fernet import Fernet

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
    def __init__(self, key: str) -> None:
        self.fernet = Fernet(key)

        self.db = sqlite3.connect(FILE_NAME)

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
                Suspicious BOOLEAN NOT NULL CHECK (Suspicious IN (0, 1))
            )
        """

        cursor.execute(create_logs_table_query)
        self.db.commit()

    def init_user_database_if_needed(self) -> None:
        cursor = self.db.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS USERS (
            id TEXT PRIMARY KEY,
            f_name TEXT NOT NULL,
            l_name TEXT NOT NULL,
            level INTEGER NOT NULL,
            username TEXT NOT NULL UNIQUE,
            registration_date DATE NOT NULL,
            hashed_pass TEXT NOT NULL
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
                starter_data,
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

    def log(self, username: str, desc: str, add_info: str, suspicious: bool):
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

        cursor.execute(
            """
            SELECT * FROM USERS 
            WHERE LOWER(username) = ? AND hashed_pass = ?
        """,
            (username.lower(), hashed),
        )

        user = cursor.fetchone()
        if user:
            return self._user_dict_from_tuple(user)
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
        return self._user_dict_from_tuple(user)

    def updateAcount(self, updatedAcount: dict):
        cursor = self.db.cursor()

        values = tuple(
            updatedAcount[key]
            for key in updatedAcount.keys()
            if key not in ["id", "type"]
        )
        values += (updatedAcount["id"],)
        set_clause = ", ".join(
            [f"{key} = ?" for key in updatedAcount.keys() if key not in ["id", "type"]]
        )

        table = "USERS" if updatedAcount["type"] == PersonType.USER else "MEMBERS"

        update_query = f"""
            UPDATE {table}
            SET {set_clause}
            WHERE id = ?
        """
        print(update_query)
        print(updatedAcount)
        cursor.execute(update_query, tuple(values))
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
        cursor.execute(
            """
                INSERT INTO USERS (id, f_name, l_name, level, username, registration_date, hashed_pass)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            user,
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
        cursor.execute("SELECT * FROM USERS LIMIT 50")
        raw_users = cursor.fetchall()

        cursor.execute("SELECT * FROM MEMBERS LIMIT 50")
        raw_members = cursor.fetchall()

        return self._user_dicts_from_tuples(raw_users) + self._member_dicts_from_tuples(
            raw_members
        )

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

    def close(self):
        self.db.commit()
        self.db.close()

        print("Safely exited!")

    def make_backup(self):
        with open(FILE_NAME, "rb") as db_file:
            decrypted_data = db_file.read()

        inpath = f"./_temp/{FILE_NAME}"  # uniquemeal.db
        outpath = "./backups/" + datetime.now().strftime("%Y-%m-%d.%H-%M-%S") + ".zip"
        with open(inpath, "wb") as file:
            file.write(decrypted_data)

        with zipfile.ZipFile(outpath, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(inpath, os.path.basename(inpath))


    def restore_backup(current_user, file_name):
            # Constants
        BACKUP_FOLDER = "./backups"
        DATABASE_FILE = "uniquemeal.db"  # Adjust based on your backup file naming
        backup_file = input("Enter the name of the backup file to restore (including .zip): ")

        if Connection.has_null_byte(backup_file):
            print("Invalid backup file name. Null bytes detected.")
            time.sleep(10)
            return

        # Validate backup file format
        if not Connection.validate_backup_file(backup_file):
            print("Invalid backup file name. Backup format error.")
            time.sleep(10)
            return

        try:
            # Get the path to the backup zip file
            backup_path = os.path.join(BACKUP_FOLDER, backup_file)

            # Check if the backup file exists
            if not os.path.exists(backup_path):
                print("Backup file not found.")
                return
            
            # Create a temporary directory for extraction
            temp_dir = "./_temprestore"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)  # Create the directory if it doesn't exist
                print("Temporary directory created.")

            # Extract the backup zip file
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extract(DATABASE_FILE, temp_dir)
            
            extracted_db_path = os.path.join(temp_dir, DATABASE_FILE)
            print(f"Extracted to: {extracted_db_path}")
            time.sleep(2)
            # Step 1: Backup current database
            current_db_path = os.path.join(BACKUP_FOLDER, DATABASE_FILE)
            print(f"Extracted to: {current_db_path}")

            print("derde")
            time.sleep(2)
            # backup_db_path = os.path.join(Connection.BACKUP_FOLDER, f"backup_{time.strftime('%Y%m%d_%H%M%S')}.db")
            # if os.path.exists(current_db_path):
            #     os.rename(current_db_path, backup_db_path)
            #     print(f"Current database backed up to: {backup_db_path}")
            # time.sleep(10)
            # Step 2: Restore the new database
            #os.rename(extracted_db_path, current_db_path)

            print("Database restored successfully.")
            time.sleep(10)

            # Step 3: Connect to the restored database
            db = sqlite3.connect(current_db_path)
            # You can add logic here to run any required SQL statements to finalize restoration if necessary

            # Close the database connection
            db.close()

            # Step 4: Cleanup temporary files
            # for file in os.listdir(temp_dir):
            #     os.remove(os.path.join(temp_dir, file))
            # os.rmdir(temp_dir)  # Remove the temp directory after cleanup
            # print("Temporary files cleaned up.")

            print("System backup restored successfully.")
            time.sleep(10)

        except Exception as e:
            print(f"Error restoring system backup: {str(e)}")
