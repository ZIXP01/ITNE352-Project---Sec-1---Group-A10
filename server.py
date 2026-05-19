import socket
import threading
import json
from api_handler import (
search_by_name,
 filter_by_category,
 filter_by_area,
 filter_by_ingredient,
 random_recipe,
 lookup_by_id
)
from cache import load_reference_cache
# Server settings
HOST = "0.0.0.0"
PORT = 12345
# Load cache when server starts
reference_cache = load_reference_cache()
print("Reference cache loaded.")
# Handle each connected client
def handle_client(client_socket, address):
 print(f"New connection from {address}")
 try:
  # Receive client name
   client_name = client_socket.recv(1024).decode()
    print(f"Client connected: {client_name}")
     while True:
     # Receive request from client
     request_data = client_socket.recv(4096).decode()
  if not request_data:
 break
# Convert JSON string to Python dictionary
 request = json.loads(request_data)
 request_type = request.get("type")
response = {}
# Search by recipe name
 if request_type == "search_name":
   keyword = request.get("keyword")
    meals = search_by_name(keyword)
    response = {
 "meals": meals[:15]
                }
# Filter by category
  elif request_type == "filter_category":
category = request.get("category")
 meals = filter_by_category(category)
response = {   "meals": meals[:15]       }
 # Filter by area
 elif request_type == "filter_area":
 area = request.get("area")
meals = filter_by_area(area)
response = {  "meals": meals[:15]}
     # Filter by ingredient
      elif request_type == "filter_ingredient":
       ingredient = request.get("ingredient")
       meals = filter_by_ingredient(ingredient)
