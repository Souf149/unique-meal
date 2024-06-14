from time import sleep
from models.connection import Connection
from tools.tools import print_user_without_pass, user_input

def list_users(db: Connection, user: dict):
    users = db.getAllUsersFromLevelAndLower(user["level"])
    print(len(users))
    while True:
        for i, _user in enumerate(users):
            print(f"{i + 1}). {_user['f_name']} {_user['l_name']}")
        
        

        print("Choose the number of the user you want to list.")
        print("To start looking for a user press f")

        choice = user_input()
        if choice.lower() == "f":
            print("LOOKING FOR USER...")
            term = user_input("Input text that we will look for: ")
            found_users = db.searchForUsers(term)
            if len(found_users) == 0:
                print("No users found")
                continue
            
            print("These users have been found: ")
            for i, _user in enumerate(found_users):
                print(f"{i + 1}). {_user['f_name']} {_user['l_name']}")
        

        
        
        if choice.isdigit():
            try:
                chosen_user = users[int(choice) - 1]
                print_user_without_pass(chosen_user)    
                sleep(1)
                return # end of looking
            except Exception as e:
                print("That is not a valid option")
                print(e)
        else:
            print("That is not a valid option")
            break