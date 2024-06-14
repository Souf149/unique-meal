from time import sleep
from models.connection import Connection
from tools.tools import print_user_without_pass, user_input
from tools.validators import is_valid




def edit_user(db: Connection, user: dict):

    while True:
        user_id = user_input("Please input the ID of the user you'd like to edit\nPress q to quit.")
        
        if user_id.lower() == "q":
            return
        
        victim = db.getUserFromId(user_id)


        if victim == None:
            print("This id does not exist, please enter a valid one")
            continue
        
        print_user_without_pass(victim)
        choice = user_input("Is this the user you want to edit? Please input yes or no")
        if choice[0].lower() == "y":
            break
        else:
            continue
    
    keys = victim.keys()
    while True:
        chosen_field = user_input("What field would you like to edit?")

        if chosen_field in keys:
            break
        print("Please choose a valid field")
    
    while True:
        new_value = user_input("What would you like this field to become?")
        if is_valid(chosen_field, new_value):
            user[chosen_field] = new_value
            db.updateUser(user)
            print("Field has been updated!")
            sleep(1)
            return
        print("That is not a valid input, please try again")