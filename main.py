import sqlite3
from models.connection import Connection


db = Connection()

while True:
    user = None
    username = input("Give your username please: ")
    password = input("Give your password please: ")
    user = db.getUserFromLogin(username, password)

    if user == None:
        print("wrong login")
        continue

    while True:
        print(f"Welcome {user['f_name']}!")
        input("...")