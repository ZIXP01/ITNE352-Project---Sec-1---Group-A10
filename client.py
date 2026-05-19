# client.py
# Main client script
import socket
import json

from menus import main_menu, recipes_menu, reference_menu
from display import (
    display_recipe_list,
    display_recipe_details,
    display_categories,
    display_areas,
    display_ingredients
)

# Server configuration
def send_request(client_socket, request_data):
    """
    Convert Python dictionary to JSON
    and send it to the server.
    """
    request_json = json.dumps(request_data)
    client_socket.send(request_json.encode())

# Receive response from server
def receive_response(client_socket):
    """
    Receive data from server and
    convert JSON back to dictionary.
    """
    response = client_socket.recv(65536).decode()
    return json.loads(response)
# Main program
def main():

    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    client_socket.connect((SERVER_IP, SERVER_PORT))

    print("Connected to server successfully.\n")

    # Ask user for username
    username = input("Enter your username: ")

    # Send username to server
    send_request(client_socket, {
        "type": "username",
        "username": username
    })

    while True:

        choice = main_menu()

        # Browse Recipes

 if choice == "1":

            while True:
                recipe_choice = recipes_menu()
                if recipe_choice == "1":
                    keyword = input("Enter recipe name keyword: ")

 send_request(client_socket, {
    "type": "search_name",
     "keyword": keyword
                    })

 response = receive_response(client_socket)

display_recipe_list(response)

# Ask user for recipe ID

meal_id = input("Enter Meal ID for full details: ")
   send_request(client_socket, {
               "type": "meal_details",
                "meal_id": meal_id
                    })

details = receive_response(client_socket)
display_recipe_details(details)

# Filter by category

 elif recipe_choice == "2":
            category = input("Enter category: ")
            send_request(client_socket, {
              "type": "filter_category",
              "category": category
             })

response = receive_response(client_socket)
display_recipe_list(response)
meal_id = input("Enter Meal ID for full details: ")
 send_request(client_socket, {
          "type": "meal_details",
           "meal_id": meal_id
                    })
details = receive_response(client_socket)
display_recipe_details(details)

# Filter by area

elif recipe_choice == "3":
        area = input("Enter area/cuisine: ")
        send_request(client_socket, {
           "type": "filter_area",
            "area": area
                    })
response = receive_response(client_socket)
display_recipe_list(response)
meal_id = input("Enter Meal ID for full details: ")
send_request(client_socket, {
   "type": "meal_details",
   "meal_id": meal_id
                    })
details = receive_response(client_socket)
display_recipe_details(details)

# Filter by ingredient

elif recipe_choice == "4":

        ingredient = input("Enter ingredient: ")
        send_request(client_socket, {
           "type": "filter_ingredient",
           "ingredient": ingredient
         })
response = receive_response(client_socket)
display_recipe_list(response)

 meal_id = input("Enter Meal ID for full details: ")

send_request(client_socket, {
                        "type": "meal_details",
                        "meal_id": meal_id
                    })
details = receive_response(client_socket)
display_recipe_details(details)

 # Random recipe

 elif recipe_choice == "5":
                    send_request(client_socket, {
                        "type": "random_recipe"
                    })
response = receive_response(client_socket)
display_recipe_details(response)
      
# Back
            
elif recipe_choice == "6":
 break
else:
  print("Invalid option.\n")

# Reference Lists
        elif choice == "2":
            while True:
                reference_choice = reference_menu()

# Categories
                if reference_choice == "1":
                    send_request(client_socket, {
                        "type": "categories"
                    })

response = receive_response(client_socket)
display_categories(response)

 # Areas

elif reference_choice == "2":
  send_request(client_socket, {
     "type": "areas"
                    })

response = receive_response(client_socket)
display_areas(response)
# Ingredients
                elif reference_choice == "3":
                    send_request(client_socket, {
                        "type": "ingredients"
                    })
response = receive_response(client_socket)
display_ingredients(response)

# Back

elif reference_choice == "4":
    break
  else:
     print("Invalid option.\n")

# Quit
    
        elif choice == "3":
            send_request(client_socket, {
                "type": "quit"
            })

print("Disconnected from server.")
client_socket.close()
break
        else:
            print("Invalid option.\n")
            
# Run program
main()


