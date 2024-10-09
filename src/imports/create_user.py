
import re
from time import sleep
from models.connection import Connection
from models.user import Level, create_user_tuple, generate_id, generate_password, hash_password
from tools.tools import check_password, user_input, clear_terminal_with_title
from datetime import datetime
from imports.validator import User_Info_Validator
from imports import helper_functions
import os

def choose_city():
    city_list = [
    "amsterdam", "rotterdam", "utrecht", "breda", "eindhoven",
    "groningen", "maastricht", "leiden", "tilburg", "almere"
    ]
    print("Please choose a city from the list below by entering the number next to it:")
    for i, city in enumerate(city_list, 1):
        print(f"{i}. {city}")

    while True:
        try:
            choice = int(input("Enter a number from 1-10: "))
            print(choice)
            if 1 <= choice <= 10:
                return city_list[choice - 1]
            else:
                print("Invalid choice. Please choose a number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def create_new_user(db: Connection, user: dict, max_level: Level):
    Validator = User_Info_Validator
    while True:
        message = ""
        while True:
            clear_terminal_with_title()
            if (message):
                print(message)
            f_name = user_input("Input first name please")
            if (Validator.validate_name(f_name)):
                message = ""
                break
            else:
                message ="Invalid option! Example: mark"

        while True:
            clear_terminal_with_title()
            if (message):
                print(message)
            l_name = user_input("Input last name please")
            if (Validator.validate_name(l_name)):
                message = ""
                break
            else:
                message = "Invalid option! Example: zuckerberg"

        while True:
            clear_terminal_with_title()
            if (message):
                print(message)
            age = user_input("Input a valid age please")
            if (Validator.validate_age(age)):
                message = ""
                break
            else:
                message = "Invalid option. Your age has to be between 0 and 120"

        while True:
            clear_terminal_with_title()
            if (message):
                print(message)
            gender = user_input("Input 'f' or 'm' to choose the gender")
            if (Validator.validate_gender(gender)):
                message = ""
                break
            else:
                message = "Invalid option!"

        while True:
            clear_terminal_with_title()
            if (message):
                print(message)
            weight = user_input("Input the weight")
            if (Validator.validate_weight(weight)):
                message = ""
                break
            else:
                message = "Incorrect weight number! Weight has to be a number between 0 and 300kg! Example: 75kg , 75.6kg"

        while True:
            clear_terminal_with_title()
            if (message):
                print(message)
            street = user_input("Input the street name")
            if (Validator.validate_street_name(street)):
                message = ""
                break
            else:
                message = "Incorrect street name! Example: Dominee Jan Scharpstraat"

        while True:
            clear_terminal_with_title()
            if (message):
                print(message)
            house_number = user_input("Input the house number")
            if (Validator.validate_housenumber(house_number)):
                message = ""
                break
            else:
                message = "Incorrect house number! house number has to be any number for 0 - 9999 "

        while True:
            clear_terminal_with_title()
            if (message):
                print(message)
            zip = user_input("Input the zipcode. \n Example: Zip Code (DDDDXX) - only enter DDDDXX ")
            if (Validator.validate_zip(zip)):
                message = ""
                break
            else:
                message = "Incorrect zip number! Example: 5353EK"

        while True:
            clear_terminal_with_title()
            if (message):
                print(message)
            city = choose_city() 
            if (Validator.validate_name(city)):
                print(f"Chosen city{city}")
                break
            else:
                message = "Incorrect city name! Choose from [1] to [10]"


        while True:
            clear_terminal_with_title()
            if(message):
                print(message)
            email = user_input("Input the emailaddress.")
            if (Validator.validate_email(email)):
                message = ""
                break
            else:
                message = "Incorrect e-mailaddress! Example: markzuckerburg@gmail.com | markzuckerburg_@hotmail.com | markzuckerburg@yahoo.com"

        while True:
            clear_terminal_with_title()
            if(message):
                print(message)
            phone = user_input("Input the phone number.\nExample: (+31-6-DDDDDDDD) - only enter DDDDDDDD '")
            if (Validator.validate_phone(phone)):
                message = ""
                break
            else:
                message = "Incorrect phone number! Only type the 8 digits after the +316 "

        while True:#souf heeft deze verbeterd | vanaf hier morgen verder testen
            if (user['level'] < 3):
                registration_date = regis_date = datetime.datetime.today().year - 2000
                break # mogelijk bij alle levels
            registration_date = user_input("Input the registration date. Example: 2001-09-11")
            if (Validator.validate_registration_date(registration_date)):
                break

        while True:
            clear_terminal_with_title()
            if (message):
                print(message)
            password = user_input("Input the password.\nmust be unique and have a length of at least 8 characters\nmust be no longer than 10 characters\nmust be started with a letter or underscores (_)\ncan contain letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (.)\nno distinguish between lowercase or uppercase letters")
            if (Validator.validate_password(password)):
                message = ""
                break
            else:
                message = "Incorrect password! Follows the instructions on how to construct a password"

        hashed_pass = hash_password(password) 

        while True:
            clear_terminal_with_title()
            if (message):
                print(message)
            level = user_input(f"What level should this user have access to?. Important: You can only make users of level: {user['level']} and lower")
            if (Validator.validate_level(level, user)):
                message = ""
                break
            else:
                message = "Incorrect level! Following the instructions of the user levels you can make"

        while True:
            clear_terminal_with_title()
            if (message):
                print(message)
            print("For the final info, please choose a name for the user.\nmust be unique and have a length of at least 8 characters\nmust be no longer than 10 characters\nmust be started with a letter or underscores (_)\ncan contain letters (a-z), numbers (0-9), underscores (_), apostrophes ('), and periods (.)\nno distinguish between lowercase or uppercase letters")
            username = user_input("Input the username")
            if (Validator.validate_username(username)):
                message = ""
                break
            else:
                message = "Incorrect username! Follows the instructions on how to construct an username"

        while True:
            membershipnumber = helper_functions.generate_id()
            membership_id = Validator.validate_id(helper_functions.generate_id()) # membershipID 
            if (membership_id):
                break
        db.addUser(create_user_tuple(generate_id(), level, f_name, l_name, age, gender, weight, street,
                   house_number, zip, city, email, phone, registration_date, username, hashed_pass)) #ID = membership_id
        db.log(user["username"], "Created new user",
               f"Created user: {username}", False)

        print("User has been created!")
        print("The password of this user is: " + password)
        sleep(1)
        return