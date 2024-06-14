from enum import Enum
from models.user import create_user, generate_id, Level, hash_password
from datetime import date


class Connection():

    def __init__(self) -> None:
        self.db = None
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

    def getAllUsersFromLevelAndLower(self, level: Level) -> list[dict]:
        users = []
        for user in self.mock_db["users"]:
            if user["level"].value >= level.value:
                users.append(user)
        return users
    
    def searchForUsers(self, term: str) -> list[dict]:
        raise NotImplementedError() # Not wasting time on implementing it on dictionaries when we have to do it on sqllite3 anwyays