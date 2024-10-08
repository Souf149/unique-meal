import re
from time import sleep
from imports.connection import Connection
from models.user import (
    Level,
    create_user_tuple,
    generate_id,
    generate_password,
    hash_password,
)
from tools.tools import check_password, user_input, clear_terminal_with_title
from datetime import datetime
from imports.validator import User_Info_Validator
from imports import helper_functions
import os


def choose_city():
    city_list = [
        "Amsterdam",
        "Rotterdam",
        "Utrecht",
        "The Hague",
        "Eindhoven",
        "Groningen",
        "Maastricht",
        "Leiden",
        "Tilburg",
        "Almere",
    ]
    print("Please choose a city from the list below by entering the number next to it:")
    for i, city in enumerate(city_list, 1):
        print(f"{i}. {city}")

    while True:
        try:
            choice = int(input("Enter a number from 1-10: "))
            if 1 <= choice <= 10:
                return city_list[choice - 1]
            else:
                print("Invalid choice. Please choose a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def create_new_user(db: Connection, user: dict, max_level: Level):
    # clear_terminal_with_title()
    Validator = User_Info_Validator
    while True:
        while True:
            clear_terminal_with_title()
            f_name = user_input("Input first name please")
            if Validator.validate_name(f_name):
                break
            else:
                print("Invalid option! Example: Mark")

        while True:
            l_name = user_input("Input last name please")
            if Validator.validate_name(l_name):
                break

        while True:
            age = user_input("Input a valid age please")
            if Validator.validate_age(age):
                break
            else:
                print("Invalid option. Your age has to be between 0 and 120")

        while True:
            gender = user_input("Input 'f' or 'm' to choose the gender")
            if Validator.validate_gender(gender):
                break
            else:
                print("Invalid option!")

        while True:
            weight = user_input("Input the weight")
            if Validator.validate_weight(weight):
                break

        while True:
            street = user_input("Input the street name")
            if Validator.validate_name(street):
                break
            else:
                print("Incorrect street name!")

        while True:
            house_number = user_input("Input the house number")
            if Validator.validate_housenumber(house_number):
                break

        while True:
            zip = user_input(
                "Input the zipcode. \n Example: Zip Code (DDDDXX) - only enter DDDDXX "
            )
            if Validator.validate_zip(zip):
                break

        while True:
            city = choose_city()
            if Validator.validate_name(city):
                print(f"Chosen city{city}")
                break

        while True:
            email = user_input("Input the emailaddress.")
            if Validator.validate_email(email):
                break

        while True:
            phone = user_input(
                "Input the phone number.\nExample: (+31-6-DDDDDDDD) - only enter DDDDDDDD '"
            )
            if Validator.validate_phone(phone):
                break

        while True:
            if user["level"] < 3:
                registration_date = regis_date = datetime.datetime.today().year - 2000
                break  # mogelijk bij alle levels
            registration_date = user_input(
                "Input the registration date. Example: 2001-09-11"
            )
            if Validator.validate_registration_date(registration_date):
                break

        while True:
            password = user_input(
                "Input the password.\nmust be unique and have a length of at least 8 characters\nmust be no longer than 10 characters\nmust be started with a letter or underscores (_)\ncan contain letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (.)\nno distinguish between lowercase or uppercase letters"
            )
            if Validator.validate_password(password):
                break

        hashed_pass = hash_password(password)  # komt nog

        while True:
            level = user_input(
                f"What level should this user have access to?. Important: You can only make users of level: {user['level']}"
            )
            if Validator.validate_level(level, user):
                break

        while True:
            print(
                "For the final info, please choose a name for the user.\nmust be unique and have a length of at least 8 characters\nmust be no longer than 10 characters\nmust be started with a letter or underscores (_)\ncan contain letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (.)\nno distinguish between lowercase or uppercase letters"
            )
            username = user_input("Input the username")
            if Validator.validate_username(username):
                break
        while True:
            membershipnumber = helper_functions.generate_id()
            membership_id = Validator.validate_id(
                helper_functions.generate_id()
            )  # membershipID
            if membership_id:
                break
        db.addUser(
            create_user_tuple(
                generate_id(),
                level,
                f_name,
                l_name,
                age,
                gender,
                weight,
                street,
                house_number,
                zip,
                city,
                email,
                phone,
                registration_date,
                username,
                hashed_pass,
            )
        )  # ID = membership_id
        db.log(user["username"], "Created new user", f"Created user: {username}", False)

        print("User has been created!")
        print("The password of this user is: " + password)
        sleep(1)
        return
