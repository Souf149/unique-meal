
from datetime import datetime
import os
import re
from time import sleep
from models.connection import Connection
from models.user import Level, create_user, generate_id, generate_password, hash_password
from tools.tools import check_password, user_input
import cryptography
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from functionalities import Encryption



# Ensure keys are generated and saved
if not os.path.exists("private_key.pem") or not os.path.exists("public_key.pem"):
    private_key_pem, public_key_pem = Encryption.generate_keys()
    Encryption.save_key("private_key.pem", private_key_pem)
    Encryption.save_key("public_key.pem", public_key_pem)
    print("Keys generated and saved to 'private_key.pem' and 'public_key.pem'")
else:
    print("Keys already exist. Loading keys.")
    
public_key = Encryption.load_public_key("public_key.pem")

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

            # Rule 4: Check if username contains only allowed characters
            if not re.match(r'^[a-zA-Z0-9_.\']+$', username):
                continue

            if db.usernameExist(username):
                print("Username exists already")
                continue

            break

        while True:
            level = user_input("What level should this user have access to? ( Please choose one of these numbers )\n1). SUPER ADMIN\n2). SYSTEM ADMIN\n3). CONSULTANT\n4). MEMBER")
            if level == "1":
                level = Level.SUPER_ADMINISTRATOR
                break
            if level == "2":
                level = Level.SYSTEM_ADMINISTRATORS
                break
            if level == "3":
                level = Level.CONSULTANT
                break
            if level == "4":
                level = Level.MEMBER
                break
            
        print("User has been created!")
        print("The password of this user is: " + password)
        sleep(1)
        # Encrypt sensitive data
        encrypted_f_name = Encryption.encrypt_message(public_key, f_name.encode())
        encrypted_l_name = Encryption.encrypt_message(public_key, l_name.encode())
        encrypted_email = Encryption.encrypt_message(public_key, email.encode())
        encrypted_phone = Encryption.encrypt_message(public_key, phone.encode())
        encrypted_street = Encryption.encrypt_message(public_key, street.encode())
        encrypted_house_number = Encryption.encrypt_message(public_key, house_number.encode())
        encrypted_zip_code = Encryption.encrypt_message(public_key, zip.encode())
        encrypted_city = Encryption.encrypt_message(public_key, city.encode())

        db.addUser(create_user(generate_id(), level, encrypted_f_name, encrypted_l_name, age, gender, weight, encrypted_street,
                   encrypted_house_number, encrypted_zip_code, encrypted_city, encrypted_email, encrypted_phone, registration_date, username, hashed_pass))
        
        break
