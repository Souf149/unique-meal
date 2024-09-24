
import re
from time import sleep
from models.connection import Connection
from models.user import Level, create_user_tuple, generate_id, generate_password, hash_password
from tools.tools import check_password, user_input
from datetime import datetime
from functionalities.validator import User_Info_Validator

def create_new_user(db: Connection, user: dict, max_level: Level):
    Validator = User_Info_Validator
    while True:
        while True:
            f_name = user_input("Input first name please")
            if (Validator.validate_name(f_name)):
                break

        while True:
            l_name = user_input("Input last name please")
            if (Validator.validate_name(l_name)):
                break

        while True:
            age = user_input("Input a valid age please")
            if (Validator.validate_age(age)):
                break

        while True:
            gender = user_input("Input 'f' or 'm' to choose the gender")
            if (Validator.validate_gender(gender)):
                break

        while True:
            weight = user_input("Input the weight")
            if (Validator.validate_weight(weight)):
                break

        while True:
            street = user_input("Input the street name")
            if (Validator.validate_name(weight)):
                break

        while True:
            house_number = user_input("Input the house number")
            if (Validator.validate_housenumber(house_number)):
                break

        while True:
            zip = user_input("Input the zipcode")
            if (Validator.validate_zip(zip)):
                break

        while True:
            city = user_input("Input the city's name")
            if (Validator.validate_name(city)):
                break

        while True:
            email = user_input("Input the emailaddress")
            if (Validator.validate_email(email)):
                break

        while True:
            phone = user_input("Input the phone number")
            if (Validator.validate_phone(phone)):
                break

        while True:
            registration_date = user_input("Input the registration date")
            if (Validator.validate_registration_date(registration_date)):
                break

        while True:
            password = user_input("Input the password")
            if (Validator.validate_password(password)):
                break

        hashed_pass = hash_password(password) # komt nog

        while True:
            print("For the final info, please choose a name for the user")
            username = user_input("Input the password")
            if (Validator.validate_username(username)):
                break

        while True:
            level = user_input("What level should this user have access to?")
            if (Validator.validate_level(level)):
                break

        db.addUser(create_user_tuple(generate_id(), level, f_name, l_name, age, gender, weight, street,
                   house_number, zip, city, email, phone, registration_date, username, hashed_pass))
        db.log(user["username"], "Created new user",
               f"Created user: {username}", False)

        print("User has been created!")
        print("The password of this user is: " + password)
        sleep(1)
        return