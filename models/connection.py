from enum import Enum
from models.user import create_user, generate_id, Level, hash_password
from datetime import date
import sqlite3
from sqlite3 import Error
from models.user import Level


class Connection():

    def __init__(self, databaseFile) -> None:
        self.db = databaseFile
        
        self.mock_db = {"users": [
            create_user("2400000000", Level.SUPER_ADMINISTRATOR, "teacher", "INF", 31, "m", 70.2, "wijnhaven", "207", "4294",
                        "Rotterdam", "cmi@hr.nl", "+31-6-12345678", date(2023, 3, 1), "teacher23", hash_password("Admin_123?")),
            create_user(generate_id(), Level.SYSTEM_ADMINISTRATORS, "Soufyan", "Abdell", 25, "m", 257, "otherstreet", "134",
                        "2342", "Dordrecht", "0963595@hr.nl", "+31-6-21424244", date(2023, 3, 3), "souf149", hash_password("a")),
            create_user(generate_id(), Level.CONSULTANT, "Reajel", "Cic", 26, "m", 50, "boringstreet", "24", "2556",
                        "Pap", "1535233@hr.nl", "+31-6-11141111", date(2024, 6, 7), "captainxx", hash_password("a")),
            create_user(generate_id(), Level.MEMBER, "Cynthia", "Amel", 19, "f", 52, "lijnbaan", "2", "1111",
                        "Pap", "1534433@hr.nl", "+31-6-22141111", date(2024, 7, 6), "flower", hash_password("ab")),
        ]
        }

    def createMembersTable(self):
        create_query =  """
        CREATE TABLE IF NOT EXISTS members (
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
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            registration_date DATE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            hashed_pass TEXT NOT NULL
        )
        """
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute(create_query)
        conn.commit()
        cursor.close()
        conn.close()

    def createUsersTable(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            registration_date DATE NOT NULL,
            role TEXT CHECK(role IN ('admin', 'consultant', 'superadmin')) NOT NULL,
            temp BOOLEAN NOT NULL CHECK(temp IN (0, 1))
        )
        """
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()
        cursor.execute(create_query)
        conn.commit()
        cursor.close()
        conn.close()

    def initSuperadmin(self):
        conn = sqlite3.connect(self.databaseFile)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'SUPER_ADMINISTRATOR'")
        user_exists = cursor.fetchone()[0] > 0

        if not user_exists:
            query = "INSERT INTO users (first_name, last_name, username, password, registration_date, role, temp) VALUES (?, ?, ?, ?, ?, ?, ?)"
            parameters = ("Reajel", "Cicilia", "SUPER_ADMINISTRATOR", "Admin_123?", date.today().strftime("%Y-%m-%d"), "superadmin", False)
            cursor.execute(query, parameters)
            conn.commit()
        else:
            pass

        cursor.close()
        conn.close()

    def getUserFromUsername(self, name: str):
        for user in self.mock_db["users"]:
            if user["name"] == name:
                return user
        return None

    def getUserFromLogin(self, username, password):
        hashed = hash_password(password)
        for user in self.mock_db["users"]:
            if user["username"].lower() == username.lower() and user["hashed_pass"] == hashed:
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

    #def addUser(self, user: dict):
     #   self.mock_db["users"].append(user)

    def addUser(self, user: dict):
        if not self.table_exists('members'):
            print("Members table does not exist, creating table...")
            self.createMembersTable()
        
        conn = sqlite3.connect(self.db)
        query = """
        INSERT INTO members (id, level, f_name, l_name, age, gender, weight, street, house_number, zip, city, email, phone, registration_date, username, hashed_pass)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        parameters = (
            user["id"], user["level"].value, user["f_name"], user["l_name"], user["age"], 
            user["gender"], user["weight"], user["street"], user["house_number"], user["zip"], 
            user["city"], user["email"], user["phone"], user["registration_date"], 
            user["username"], user["hashed_pass"]
        )
        cursor = conn.cursor()

        try:
            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()
            conn.close()
            return "OK"
        except sqlite3.Error as e:
            print("An error occurred while creating the member:", e)
            cursor.close()
            conn.close()
            return None


    def getAllUsersFromLevelAndLower(self):
        users = []
        for user in self.db["users"]:
            if user["level"].value >= level.value:
                users.append(user)
        return users
    

    def searchForUsers(self, term: str) -> list[dict]:
        raise NotImplementedError()
    
    def searchMember(self, search_key):
        try:
            conn = sqlite3.connect(self.databaseFile)
            cursor = conn.cursor()
            query = """
            SELECT * FROM members 
            WHERE 
                id LIKE ? OR
                first_name LIKE ? OR
                last_name LIKE ? OR
                address LIKE ? OR
                email LIKE ? OR
                mobile LIKE ?
            """
            # Constructing search patterns for partial matches
            search_pattern = '%' + search_key + '%'
            parameters = (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern, search_pattern)
            
            cursor.execute(query, parameters)
            members = cursor.fetchall()
            cursor.close()
            conn.close()
            return members
        except sqlite3.Error as e:
            print("An error occurred while searching members:", e)
            return None
        
    


    def table_exists(self, table_name):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def getMembersFirstAndLast(self):
        conn = sqlite3.connect(self.db)
        
        if not self.table_exists('members'):
            conn.close()
            return False
        
        cursor = conn.cursor()
        query = "SELECT f_name FROM members"
        cursor.execute(query)
        
        members = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not members:  # Check if members list is empty
            return False  # Return False if no members found
        
        return members  # Return members if found

        

    def GetAllMembers(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        query = "SELECT * FROM members"
        cursor.execute(query)
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        return members
    
    def DoAllMmembersExist(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        query = "SELECT * FROM members"
        cursor.execute(query)
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        return members