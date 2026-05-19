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
 response = {
      "meals": meals[:15]}
     # Random recipe
      elif request_type == "random_recipe":
     meals = random_recipe()
response = {
     "meals": meals
                }
# Full recipe details
 elif request_type == "lookup_meal":
   meal_id = request.get("meal_id")
 meals = lookup_by_id(meal_id)
    response = {
        "meals": meals
    }
 # Categories from cache
  elif request_type == "categories":
 print("Error:", error)
    finally:
        print(f"Client disconnected: {client_name}")
        client_socket.close()
# Create TCP server socket
response = {
  "categories": reference_cache["categories"]
                }
 # Areas from cache
   elif request_type == "areas":
   response = {
   "areas": reference_cache["areas"]
                }
 # Ingredients from cache
    elif request_type == "ingredients":
      response = {
     "ingredients": reference_cache["ingredients"][:50]
                }
   # Invalid request
     else:
response = {
 "error": "Invalid request type"
                }
  # Send response to client
  client_socket.send(json.dumps(response).encode())
    except Exception as error:
 print("Error:", error)
    finally:
    print(f"Client disconnected: {client_name}")
    client_socket.close()
# Create TCP server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Server is running on port {PORT}...")
# Accept clients forever
