from time import sleep
from models.connection import Connection
from tools.tools import print_user_without_pass, user_input
from functionalities import Encryption

def list_users(connection: Connection, user: dict):
    members = connection.getMembersFirstAndLast()
    print("These are the users in the system: \n")
    while True:
        if members is False:
            print("No users found")
            return

        for member in members:
            print(f"{member[0]} {member[1]} \n\n")
            #print(members)

        #print("To start looking for a user, type the username, firstname, lastname or the ID of the user you want to find.")
        user_input = input("To start looking for a user, type the username, firstname, lastname or the ID of the user you want to find. \n\n")
        choice = user_input
        if isinstance(choice, str):  # Correcting the type check here
            print("LOOKING FOR USER...")
            found_users = connection.searchMember(choice)
            if found_users is None:
                print("No users found")
                continue

            #print("These users have been found: ")
            #for i, founduser in enumerate(found_users, start=1):
             #   print(f"User {i}: {founduser[2]} {founduser[3]} with username: {founduser[14]} and with the user ID {founduser[0]}\n")
           # print("Please choose a user by typing the number of the user you want to see more information about.")
            while True:
                try:
                    print(f"The found users are:\n\n\n")
                    print(f"{found_users}\n\n\n")
                    
                    while True:
                        ChosenUser = input("Please type the number of the wanted user: ")
                        if ChosenUser.isdigit():
                            break
                    ChosenMember = found_users[int(ChosenUser)-1]
                    #print(f"Chosen: User {ChosenUser}: {ChosenMember[2]} {ChosenMember[3]} with username: {ChosenMember[14]} and with the user ID {ChosenMember[0]}\n")
                    while True:
                        ChooseOption = input("Press 1 to edit the user or press 2 to delete the user.")
                        if ChooseOption.isdigit() and 1 <= int(ChooseOption) <= 2:
                            break

                    if ChooseOption == "1":
                        choice = int(user_input)-1
                        if 0 <= choice < len(found_users):
                            print(f"You've chosen member: {found_users[choice][14]}")
                            selected_user = found_users[choice]

                            # Display current information of the selected user
                            print(f"Current information of the selected user:")
                            print(f"First Name: {selected_user[2]}")
                            print(f"Last Name: {selected_user[3]}")
                            print(f"Username: {selected_user[14]}")
                            print(f"Email: {selected_user[4]}")
                            # Add other fields as needed

                            # Prompt for new values
                            fields_to_update = {}
                            new_first_name = input("Enter new first name (leave blank to keep current): ")
                            if new_first_name == "":
                                new_first_name = selected_user[2]
                            else:
                                fields_to_update['f_name'] = new_first_name

                            new_last_name = input("Enter new last name (leave blank to keep current): ")
                            if new_last_name == "":
                                new_last_name = selected_user[3]
                            else:
                                fields_to_update['l_name'] = new_last_name

                            new_username = input("Enter new username (leave blank to keep current): ")
                            if  new_username == "":
                                new_username = selected_user[14]
                            else:
                                fields_to_update['username'] = new_username

                            new_email = input("Enter new email (leave blank to keep current): ")
                            if new_email == "":
                                new_email = selected_user[4]
                            else:
                                fields_to_update['email'] = new_email


                            if fields_to_update:
                                result = connection.updateMember(
                                    found_users[choice][14],  # username
                                    new_first_name=new_first_name,
                                    new_last_name=new_last_name,
                                    new_username=new_username,
                                    new_email=new_email
                                )
                                if result == "OK":
                                    print("Member updated successfully.")
                                else:
                                    print("An error occurred while updating the member.")
                            else:
                                print("No changes made to the member.")

                            break
                    elif ChooseOption == "2":
                        DeleteAMember = connection.deleteMember(founduser[0])
                        if DeleteAMember == "OK":
                            print("Member deleted successfully.")
                        else:
                            print("An error occurred while deleting the member.")
                        
                    else:
                        print("Please choose a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

                    


        if choice.isdigit():
            try: #idk wat je hier probeert te doen maar ik kan hier makkelijk id based search van maken als dat is wat je wilt?
                chosen_user = users[int(choice) - 1]
                for key, value in chosen_user.items():
                    if key != "hashed_pass":
                        print(f"{key}: {value}")

                sleep(1)
                return # end of looking
            except Exception as e:
                print("That is not a valid option")
                print(e)
        else:
            print("That is not a valid option")
            break