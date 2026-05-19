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


