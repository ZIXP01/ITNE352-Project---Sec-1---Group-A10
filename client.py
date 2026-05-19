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


