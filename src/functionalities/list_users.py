from time import sleep
from models.connection import Connection
from tools.tools import print_user_without_pass, user_input, validate_number, clear_terminal_with_title
import os

def list_users(db: Connection, user: dict):
    users = db.getAllUsersFromLevelAndLower(user["level"]) 
    while True:
        clear_terminal_with_title("UNIQUE MEAL")  # Show title at the start of the menu
        print("\nPress [0] To go back to the main menu\nPress [1] To look for a user\nPress [2] To view & choose a user out of the list")
        choice = user_input()

        if choice == "1":
            clear_terminal_with_title("UNIQUE MEAL")  # Title for searching
            print("LOOKING FOR USER...")
            term = user_input("Input text that we will look for: ")
            found_users = db.searchForUsers(term)
            
            if len(found_users) == 0:
                choice = user_input("No users found. Press [0] to return to the main menu, press [1] or anything else to try again.")
                if choice == "0":
                    return
                else:
                    continue

            clear_terminal_with_title("UNIQUE MEAL")  # Title for search results
            print("These users have been found: ")
            for i, _user in enumerate(found_users):
                print(f"{i + 1}). {_user['f_name']} {_user['l_name']}")
            
            choice = user_input("Type the number of the user you want to read information of")

        elif choice == "2":
            while True:
                clear_terminal_with_title("UNIQUE MEAL")  # Title before listing users
                print("List of Users:\n")
                for i, _user in enumerate(users):
                    print(f"{i + 1}). {_user['f_name']} {_user['l_name']}")
                chosen_user = validate_number("Choose the number of the user you'd like to view the information of: ")

                if 1 <= int(chosen_user) <= len(users):              
                    try:
                        chosen_user = users[int(chosen_user) - 1]
                        clear_terminal_with_title("UNIQUE MEAL")  # Title for user info
                        print_user_without_pass(chosen_user)

                        choice = int(user_input("Type [0] to return to the main menu. \nType [1] or anything else to list another user's information"))
                        
                        if choice != 0:
                            continue  
                        else:
                            return  

                    except Exception as e:
                        print("An error occurred while processing the user data.")
                        print(e)
                        break
                else:
                    print("Incorrect list number, try again!")
                    
        elif choice == "0":
            break
        
        else:
            print("That is not a valid option!")
            sleep(2)
