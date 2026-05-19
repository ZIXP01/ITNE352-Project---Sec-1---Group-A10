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


