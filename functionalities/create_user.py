
from datetime import datetime
import re
from time import sleep
from models.connection import Connection
from models.user import Level, create_user_tuple, generate_id, generate_password, hash_password
from tools.tools import check_password, user_input


def create_new_user(db: Connection, user: dict, max_level: Level):
    while True:
        f_name = user_input("Input first name please")
        l_name = user_input("Input last name please")

        while True:
            age = user_input("Input a valid age please")
            if age.isdigit():
                age = int(age)
                break

        while True:
            gender = user_input("Input 'f' or 'm' to choose the gender")
            if gender == "m" or gender == "f":
                break

        while True:
            weight = user_input("Input the weight")
            try:
                weight = float(weight)
                break
            except ValueError:
                continue

        street = user_input("Input the street name")
        house_number = user_input("Input the house number")
        zip = user_input("Input the zipcode")
        city = user_input("Input the city's name")

        while True:
            email = user_input("Input the emailaddress")
            if re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)").match(email):
                break

        while True:
            phone = user_input("Input the phone number after +31-6. Input 8 digits please")
            if re.compile(r'^\d{8}$').match(phone):
                break

        registration_date = datetime.now()
        password = generate_password()
        hashed_pass = hash_password(password)

        while True:
            print("For the final info, please choose a name for the user")
            username = user_input("Input the username")

            if len(username) < 8 or len(username) > 10:
                print("Username has to be between 8 and 10 characters")
                continue

            if not re.match(r'^[a-zA-Z_]', username):
                print("Username can only start with a letter or an underscore")
                continue

            if not re.match(r'^[a-zA-Z0-9_.\']+$', username):
                continue

            if db.usernameExist(username):
                print("Username exists already")
                continue

            break

        while True:
            level = user_input("What level should this user have access to?")
            if level.isdigit() and Level.MEMBER >= int(level) >= user["level"]:
                break

        db.addUser(create_user_tuple(generate_id(), level, f_name, l_name, age, gender, weight, street,
                   house_number, zip, city, email, phone, registration_date, username, hashed_pass))
        db.log(user["username"], "Created new user", f"Created user: {username}", False)

        print("User has been created!")
        print("The password of this user is: " + password)
        sleep(1)
        return
