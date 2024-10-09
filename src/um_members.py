import traceback
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

from imports.helper_functions import (
    Level,
    clear_terminal_with_title,
    user_input,
)

from imports.connection import Connection
from functionalities.backup import backup
from functionalities.change_password import change_my_password
from functionalities.edit_user import edit_account, reset_account_password
from functionalities.list_users import list_users
from functionalities.see_logs import see_logs
from functionalities.create_account import create_new_member, create_new_user

DEBUG = True


with open("./key.key", "rb") as f:
    key = f.read()

with open("./private.key", "rb") as f:
    private_key = serialization.load_pem_private_key(
        data=f.read(),
        backend=default_backend(),
        password=None,
    )


with open("./public.key", "rb") as f:
    public_key = serialization.load_pem_public_key(
        f.read(),
    )

message = b"abcdef"

ciphertext = public_key.encrypt(  # type: ignore
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)
decrypted = private_key.decrypt(  # type: ignore
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)

print(f"""
        msg: {str(message)}
        cipphertext: {str(ciphertext)}
        decrypted: {str(decrypted)}    
      """)

clear_terminal_with_title()

db = Connection(private_key, public_key)
login_attempts = 0


try:
    while True:
        user = None
        username = user_input("Give your username please: ")
        password = user_input("Give your password please: ")
        login_attempts += 1
        user = db.getUserFromLogin(username, password)

        if user is None:
            print("wrong login")
            if login_attempts > 5:
                db.log(
                    "",
                    "Unsuccessful login.",
                    f"username: {username}. Multiple usernames and passwords are tried in a row.",
                    True,
                )
            else:
                db.log("", "Unsuccessful login.", f"username: {username}.", False)
            continue

        # SUCCESFUL LOGIN
        print(f"Logged in with the id: {user['id']}")

        while True:
            clear_terminal_with_title()

            print(f"Welcome {user['f_name']}!")
            print(f"Level: {Level.NAMES[user['level']]}!")

            print("Choose a number to select what you want to do:")
            print("1).\tChange my password")
            print("2).\tAdd a new member")
            print("3).\tModify/delete account information")
            print("4).\tSearch/retrieve account information")

            if user["level"] in [
                Level.SYSTEM_ADMINISTRATOR,
                Level.SUPER_ADMINISTRATOR,
            ]:
                print("5).\tAdd a new user")
                print("6).\tReset an existing account's password")
                print("7).\tMake/Delete a backup of the system")
                print("8).\tSee logs")

            option = user_input('Select an action or press "Q" to log out: ').lower()

            if option == "q":
                print("Logging out")
                clear_terminal_with_title()
                break

            if option == "1":
                change_my_password(db, user)
            if option == "2":
                create_new_member(db, user)
            if option == "3":
                edit_account(db, user)
            if option == "4":
                list_users(db, user)

            if user["level"] in [
                Level.SYSTEM_ADMINISTRATOR,
                Level.SUPER_ADMINISTRATOR,
            ]:
                if option == "5":
                    create_new_user(db, user)
                if option == "6":
                    reset_account_password(db, user)
                if option == "7":
                    backup(db)
                if option == "8":
                    see_logs(db)

            db.db.commit()

except KeyboardInterrupt:
    db.close()
    print("Bye bye :)")
except BaseException:
    if DEBUG:
        print(traceback.format_exc())
    db.close()
