#SERVER SIDE 
import socket 
import json 
import threading 
import urllib
import urllib.request
import urllib.error
import struct


#CONSTANTS 
HOST = "0.0.0.0"
PORT = 5555
GROUP_ID = "GROUP_10"
URL = "https://www.themealdb.com/api/json/v1/1/"

# Lock only needed for console output (shared write resource)
print_lock = threading.Lock()
def safe_print(msg: str) -> None:
    """Thread-safe console output."""
    with print_lock:
        print(msg)


# CREATE FUNCTION TO CONVERT JSON DATA TO DICT , THAT FETCH A URL AND RETURN DICT OR NONE IF AN ERROR OCCUR 
def fetch_url(url) -> dict | None:
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        safe_print(f"ERROR on fetch_url: {exc}")
        return None
 

# REFERENCE CACHE TO HANDLE THE DATA ONCE INSTEAD OF RETREIVE THE DATA MANY TIMES
reference_cache = {
    "categories": [],
    "areas": [],
    "ingredients": [] }

categories_url="list.php?c=list"
areas_url = "list.php?a=list"
ingredients_url ="list.php?i=list"


# REFERENCE CACHE LOADER ONCE AT STARTUP 

def load_reference_cache():
    safe_print("SERVER Loading reference cache from TheMealDB ...")
 
    # Categories
    data = fetch_url(URL + categories_url )
    if data and data.get("meals"):
        reference_cache["categories"] = [
            {"strCategory": m["strCategory"]} for m in data["meals"]
        ]
    safe_print(f"CACHE  Categories loaded: {len(reference_cache['categories'])} entries")
 

    # Areas
    data = fetch_url(URL + areas_url)
    if data and data.get("meals"):
        reference_cache["areas"] = [
            {"strArea": m["strArea"]} for m in data["meals"]
        ]
    safe_print(f"CACHE  Areas loaded: {len(reference_cache['areas'])} entries")
 

    # Ingredients 
    data = fetch_url(URL + ingredients_url)
    if data and data.get("meals"):
        reference_cache["ingredients"] = [
            {"strIngredient": m["strIngredient"]} for m in data["meals"]
        ]
    safe_print(f"CACHE  Ingredients loaded: {len(reference_cache['ingredients'])} entries")
 

    # Write to file (ingredients capped at 50)
    file_data = {
        "categories":  reference_cache["categories"],
        "areas":       reference_cache["areas"],
        "ingredients": reference_cache["ingredients"][:50]
    }
    filename = f"reference_{GROUP_ID}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(file_data, f, indent=2, ensure_ascii=False)
    safe_print(f"CACHE  Reference file written: {filename}")


# SOCKET MESSAGE HANDLERS WITHOUT LENGTH-PREFIXED MESSAGE FRAMING 

def send_json(conn: socket.socket, obj) -> None:
    message = json.dumps(obj) + "\n"
    conn.sendall(message.encode('utf-8'))


def recv_json(conn: socket.socket) -> dict | None:
    """Receive a newline-terminated JSON message."""
    buffer = b""
    try:
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                return None
            buffer += chunk
            if b"\n" in buffer:
                line, _ = buffer.split(b"\n", 1)
                return json.loads(line.decode('utf-8'))
    except (ConnectionResetError, json.JSONDecodeError):
        return None
    


# THE SOCKET MESSAGE HANDLER WITH THE ADDITIONAL CONCEPT (Length-prefixed message framing)
def send_message(conn: socket.socket, obj) -> None:
    """Send a JSON object preceded by a 4-byte big-endian length field."""
    data = json.dumps(obj).encode('utf-8')
    length = struct.pack(">I", len(data))  # 4 bytes, big-endian
    conn.sendall(length + data)


def recv_message(conn: socket.socket) -> dict | None:
    """Receive a length-prefixed message and return parsed JSON."""
    try:
        # Read exactly 4 bytes to get the message length
        raw_length = b""
        while len(raw_length) < 4:
            chunk = conn.recv(4 - len(raw_length))
            if not chunk:
                return None
            raw_length += chunk

        length = struct.unpack(">I", raw_length)[0]

        # Read exactly 'length' bytes for the message body
        data = b""
        while len(data) < length:
            chunk = conn.recv(length - len(data))
            if not chunk:
                return None
            data += chunk

        return json.loads(data.decode('utf-8'))
    except (ConnectionResetError, json.JSONDecodeError, struct.error):
        return None


#JSON FILE SAVER  (per-client, per-request)
def save_json(client_name: str, option: str, payload) -> None:
    """Save recipe response data to a per-client JSON file."""
    filename = f"{client_name}_{option}_{GROUP_ID}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


 
# API HELPERS

def search_by_name(keyword: str) -> list:
    data = fetch_url(URL + f"search.php?s={keyword}")
    if data and data.get("meals"):
        return data["meals"][:15]
    return []


def filter_by_category(category: str) -> list:
    data = fetch_url(URL + f"filter.php?c={category}")
    if data and data.get("meals"):
        return data["meals"][:15]
    return []


def filter_by_area(area: str) -> list:
    data = fetch_url(URL + f"filter.php?a={area}")
    if data and data.get("meals"):
        return data["meals"][:15]
    return []


def filter_by_ingredient(ingredient: str) -> list:
    data = fetch_url(URL + f"filter.php?i={ingredient}")
    if data and data.get("meals"):
        return data["meals"][:15]
    return []


def get_random_recipe() -> dict | None:
    data = fetch_url(URL + "random.php")
    if data and data.get("meals"):
        return data["meals"][0]
    return None


def get_meal_by_id(meal_id: str) -> dict | None:
    data = fetch_url(URL + f"lookup.php?i={meal_id}")
    if data and data.get("meals"):
        return data["meals"][0]
    return None


#CLIENT HANDLER  
def handle_client(conn: socket.socket, addr: tuple) -> None:
    """Handle all communication with one connected client."""
    client_name = "unknown"

    try:
        # Step 1: receive client name
        init_msg = recv_message(conn)
        if init_msg and "name" in init_msg:
            client_name = init_msg["name"].strip()
        safe_print(f"[CONNECT]  '{client_name}' connected from {addr}")
        send_message(conn, {"status": "ok", "message": f"Welcome {client_name}!"})

        # Step 2: request-response loop
        while True:
            request = recv_message(conn)
            if request is None:
                break  # client disconnected

            option  = request.get("option", "")
            param   = request.get("param", "")
            safe_print(f"[REQUEST]  {client_name} → option='{option}' param='{param}'")

            # ── Reference list requests (served from cache) ──────────────
            if option == "categories":
                safe_print(f"[CACHE]    Serving categories to {client_name}")
                send_message(conn, {"status": "ok", "data": reference_cache["categories"]})

            elif option == "areas":
                safe_print(f"[CACHE]    Serving areas to {client_name}")
                send_message(conn, {"status": "ok", "data": reference_cache["areas"]})

            elif option == "ingredients":
                safe_print(f"[CACHE]    Serving ingredients to {client_name}")
                limited = reference_cache["ingredients"][:50]
                send_message(conn, {"status": "ok", "data": limited})

            # ── Recipe requests (fetched from TheMealDB) ─────────────────
            elif option == "search":
                safe_print(f"[API]      Searching meals by name '{param}' for {client_name}")
                meals = search_by_name(param)
                save_json(client_name, "search", meals)
                send_message(conn, {"status": "ok", "data": meals})

            elif option == "filter_category":
                safe_print(f"[API]      Filtering by category '{param}' for {client_name}")
                meals = filter_by_category(param)
                save_json(client_name, "filter_category", meals)
                send_message(conn, {"status": "ok", "data": meals})

            elif option == "filter_area":
                safe_print(f"[API]      Filtering by area '{param}' for {client_name}")
                meals = filter_by_area(param)
                save_json(client_name, "filter_area", meals)
                send_message(conn, {"status": "ok", "data": meals})

            elif option == "filter_ingredient":
                safe_print(f"[API]      Filtering by ingredient '{param}' for {client_name}")
                meals = filter_by_ingredient(param)
                save_json(client_name, "filter_ingredient", meals)
                send_message(conn, {"status": "ok", "data": meals})

            elif option == "random":
                safe_print(f"[API]      Random recipe requested by {client_name}")
                meal = get_random_recipe()
                save_json(client_name, "random", meal)
                if meal:
                    send_message(conn, {"status": "ok", "data": meal})
                else:
                    send_message(conn, {"status": "error", "message": "Could not fetch random recipe."})

            elif option == "details":
                safe_print(f"[API]      Meal details for ID='{param}' requested by {client_name}")
                meal = get_meal_by_id(param)
                save_json(client_name, "details", meal)
                if meal:
                    send_message(conn, {"status": "ok", "data": meal})
                else:
                    send_message(conn, {"status": "error", "message": "Meal not found."})

            elif option == "quit":
                safe_print(f"[QUIT]     {client_name} requested disconnect")
                send_message(conn, {"status": "ok", "message": "Goodbye!"})
                break

            else:
                send_message(conn, {"status": "error", "message": f"Unknown option: {option}"})

    except Exception as exc:
        safe_print(f"[ERROR]    Exception handling {client_name}: {exc}")
    finally:
        conn.close()
        safe_print(f"[DISCONNECT] '{client_name}' disconnected.")




# MAIN DEF TO RUN THE SOCKET CREATION
def main():

    # LOAD REFERENCE CACHE BEFORE OPENING THE SOCKET 
    load_reference_cache()

    # CREATE AND BIND THE TCP SERVER SOCKET 
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST,PORT))
    server_socket.listen(5)
    safe_print(f" SERVER is running on {HOST} : {PORT} \n waiting for clients ... ")

    # ACCEPT LOOP 
    try :
        while True :
            conn , addr = server_socket.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        safe_print("SERVER shutting down ... ")

    finally : 
        server_socket.close()


if __name__=="__main__" : 
    main()
