from time import sleep
from models.connection import Connection
from tools.tools import print_user_without_pass, user_input
from tools.validators import is_valid


def edit_user(db: Connection, user: dict):

    while True:
        user_id = user_input(
            "Please input the ID of the user you'd like to edit\nPress q to quit.\nPress D to delete a user.")

        if user_id.lower() == "q":
            return

        if user_id[0] == "D":
            print("We are going to DELETE a user")
            user_id = user_input(
                "Please enter the ID of the user you want to delete.")
            victim = db.getUserFromId(user_id)
            if victim == None:
                print("User not found...")
                sleep(1)
            try:
                if victim is not None and user['level'] > victim['level']:
                    db.delete_user(user_id)
                    print("User has been deleted")
                    db.log(user['username'], "User has been deleted",
                            f"User was of level: {victim['level']}", False)
                    return
            except KeyError as e:
                print(f"Key error occurred: {e}. Please ensure that 'level' exists in the user dictionary.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")


        victim = db.getUserFromId(user_id)
        #waarom nog een keer verwijder
        if victim == None:
            print("This id does not exist, please enter a valid one")
            continue

        print_user_without_pass(victim)
        choice = user_input(
            "Is this the user you want to edit? Please input yes or no")
        if choice[0].lower() == "y":
            break
        else:
            continue

    keys = victim.keys()
    try:
        if user['level'] > victim['level']:
            while True:
                chosen_field = user_input("What field would you like to edit?")

                if chosen_field in keys and chosen_field != "hashed_pass":
                    break
                print("Please choose a valid field")
        
            while True:
                new_value = user_input("What would you like this field to become?")
                if is_valid(chosen_field, new_value):
                    user[chosen_field] = new_value
                    db.updateUser(victim)
                    db.log(user["username"], "Updated user in database",
                           f"User: {user['username']} has been edited in field: {chosen_field}", False)
                    print("Field has been updated!")
                    sleep(1)
                    return
                print("That is not a valid input, please try again")
        else:
            print(f"You can only change info of levels: {user['level']} and lower!")
    except KeyError as e:
        print(f"Key error occurred: {e}. Please ensure that 'level' exists in the user dictionary.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
