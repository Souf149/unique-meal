import sqlite3
from models.user import create_user_dict, create_user_tuple, generate_id, Level, hash_password
from datetime import date
from tools.tools import user_input
from Crypto.Cipher import Salsa20


class Connection:

    def __init__(self, key: str) -> None:
        self.cipher = Salsa20.new(key.encode())
        ciphertext =  self.cipher.encrypt(b'The secret I want to send.')
        ciphertext += self.cipher.encrypt(b'The second part of the secret.')
        print(self.cipher.nonce)  # A byte string you must send to the receiver too
        user_input()

        self.db = sqlite3.connect('users.db')
        self.init_database_if_needed()


    
    def init_database_if_needed(self) -> None:
        # Connect to SQLite database (or create it if it doesn't exist)
        cursor = self.db.cursor()

        # Create USERS table with the specified attributes if it doesn't exist
        cursor.execute('''
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
        ''')

        starter_data = [
            create_user_tuple("2400000000", Level.SUPER_ADMINISTRATOR, "teacher", "INF", 31, "m", 70.2, "wijnhaven", "207", "4294",
                        "Rotterdam", "cmi@hr.nl", "+31-6-12345678", date(2023, 3, 1), "teacher23", hash_password("Admin_123?")),
            create_user_tuple(generate_id(), Level.SYSTEM_ADMINISTRATORS, "Soufyan", "Abdell", 25, "m", 257, "otherstreet", "134",
                        "2342", "Dordrecht", "0963595@hr.nl", "+31-6-21424244", date(2023, 3, 3), "souf149", hash_password("a")),
            create_user_tuple(generate_id(), Level.CONSULTANT, "Reajel", "Cic", 26, "m", 50, "boringstreet", "24", "2556",
                        "Pap", "1535233@hr.nl", "+31-6-11141111", date(2024, 6, 7), "captainxx", hash_password("a")),
            create_user_tuple(generate_id(), Level.MEMBER, "Cynthia", "Amel", 19, "f", 52, "lijnbaan", "2", "1111",
                        "Pap", "1534433@hr.nl", "+31-6-22141111", date(2024, 7, 6), "flower", hash_password("ab")),
        ]


        cursor.execute('SELECT COUNT(*) FROM USERS')
        if cursor.fetchone()[0] == 0:
            cursor.executemany('''
            INSERT INTO USERS (id, level, f_name, l_name, age, gender, weight, street, house_number, zip, city, email, phone, registration_date, username, hashed_pass)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', starter_data)
            print("Dummy data inserted into USERS table.")
        else:
            print("USERS table already contains data. No new data inserted.")

        self.db.commit()

    def getUserFromUsername(self, name: str):
        for user in self.mock_db["users"]:
            if user["name"] == name:
                return user
        return None

    def getUserFromLogin(self, username: str, password: str) -> dict | None:
        hashed = hash_password(password)
        
        cursor = self.db.cursor()

        cursor.execute('''
            SELECT * FROM USERS 
            WHERE LOWER(username) = ? AND hashed_pass = ?
        ''', (username.lower(), hashed))

        user = cursor.fetchone()
        if user:
            return self._dict_from_tuple(user)
        return None
    
    def getUserFromId(self, id):
        for user in self.mock_db["users"]:
            if user["id"] == id:
                return user
        return None

    def updateUser(self, updatedUser: dict):
        for i, user in enumerate(self.mock_db["users"]):
            if user["id"] == updatedUser["id"]:
                self.mock_db["users"][i] = updatedUser
                return

        raise Exception("NO USER FOUND WITH THIS ID: " + updatedUser["id"])

    def usernameExist(self, username: str):
        for user in self.mock_db["users"]:
            if user["username"].lower() == username.lower():
                return True
        return False

    def addUser(self, user: dict):
        self.mock_db["users"].append(user)

    def getAllUsersFromLevelAndLower(self, level: int) -> list[dict]:

        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM USERS')
        raw_users = cursor.fetchall()

        return self._dicts_from_tuples(raw_users)
    
    def searchForUsers(self, term: str) -> list[dict]:
        raise NotImplementedError() # Not wasting time on implementing it on dictionaries when we have to do it on sqllite3 anwyays
    
    def _dict_from_tuple(self, tuple: tuple) -> dict:
        return create_user_dict(tuple)

    def _dicts_from_tuples(self, tuples: list[tuple]) -> list[dict]:
        return map(create_user_dict, tuples)

    def close(self):
        self.db.commit()
        self.db.close()