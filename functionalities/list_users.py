from time import sleep
from models.connection import Connection
from tools.tools import print_user_without_pass, user_input

def list_users(connection: Connection, user: dict):
    members = connection.getMembersFirstAndLast()
    if not members:
        print("No members found")
        return
    
    for i in range(len(members)):
        for j in range(len(members)):
            print(members[j])
        #print(f"First Name: {member[0]}, Last Name: {members[1]} AND {members}")
        
        

        print("Choose the number of the user you want to list.")#Bij dit gedeelte, doordat het in een loop zit is het toch no
        print("To start looking for a user press f")

        choice = user_input()
        if choice.lower() == "f":
            print("LOOKING FOR USER...")
            term = user_input("Input text that we will look for: ")
            found_users = connection.searchMember(term)
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