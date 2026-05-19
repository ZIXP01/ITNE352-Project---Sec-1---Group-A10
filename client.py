# client.py
# Main client script
import socket
import json

"""
Recipe Discovery System - Client Script
ITNE352: Network Programming, S2 2025-2026
Group: G12: SAYDAH ALWARD-202402042, ZABIBA AHMED-202404853
"""

# importing required packages for the client side
import socket
import json
import struct

# server configuration
HOST = '127.0.0.1'
PORT = 5555

# allowed values for validation before sending requests to server
VALID_CATEGORIES = {
    "Beef", "Chicken", "Seafood",
    "Vegetarian", "Dessert",
    "Pasta", "Breakfast"
}

VALID_AREAS = {
    "Italian", "Indian", "Mexican",
    "Japanese", "Moroccan", "British",
    "American", "Thai"
}


# -------------------------------------------------------------------
# SOCKET HANDLERS WITHOUT LENGTH-PREFIXED MESSAGE FRAMING
# -------------------------------------------------------------------

# convert dictionary into JSON then send it to the server
def send_json(conn, obj):

    data = json.dumps(obj) + "\n"
    conn.sendall(data.encode("utf-8"))


# receive JSON data until "\n" is found
def recv_json(conn):

    buffer = b""

    try:
        while True:

            chunk = conn.recv(4096)

            if not chunk:
                return None

            buffer += chunk

            if b"\n" in buffer:
                line, _ = buffer.split(b"\n", 1)
                return json.loads(line.decode("utf-8"))

    except (ConnectionResetError, json.JSONDecodeError):
        return None


# -------------------------------------------------------------------
# SOCKET HANDLERS WITH LENGTH-PREFIXED MESSAGE FRAMING
# -------------------------------------------------------------------

def send_message(conn, obj):

    # convert dictionary into JSON bytes
    payload = json.dumps(obj).encode("utf-8")

    # add 4-byte big-endian length header
    header = struct.pack(">I", len(payload))

    conn.sendall(header + payload)


def recv_message(conn):

    # receive first 4 bytes (message length)
    raw_header = b""

    while len(raw_header) < 4:

        part = conn.recv(4 - len(raw_header))

        if not part:
            return None

        raw_header += part

    # unpack message length
    message_length = struct.unpack(">I", raw_header)[0]

    # receive remaining message data
    received_data = b""

    while len(received_data) < message_length:

        part = conn.recv(message_length - len(received_data))

        if not part:
            return None

        received_data += part

    # decode and convert JSON into dictionary
    try:
        return json.loads(received_data.decode("utf-8"))

    except json.JSONDecodeError:
        return None


SEPARATOR = "=" * 55


# print formatted section title
def print_header(title):

    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


# display short recipe list
def display_meal_list(meals):

    print_header(f"RESULTS ({len(meals)} found)")

    for number, meal in enumerate(meals, start=1):

        meal_name = meal.get("strMeal", "Unknown")
        meal_id = meal.get("idMeal", "N/A")
        thumbnail = meal.get("strMealThumb", "N/A")

        print(f"  [{number:2}] {meal_name}")
        print(f"  ID: {meal_id}  |  Thumb: {thumbnail}")


# display full recipe details
def display_meal_details(meal):

    print_header("RECIPE DETAILS")

    print(f"  Name        : {meal.get('strMeal', 'N/A')}")
    print(f"  Category    : {meal.get('strCategory', 'N/A')}")
    print(f"  Area        : {meal.get('strArea', 'N/A')}")
    print(f"  Tags        : {meal.get('strTags') or 'N/A'}")
    print(f"  YouTube     : {meal.get('strYoutube') or 'N/A'}")
    print(f"  Source      : {meal.get('strSource') or 'N/A'}")

    print("\n  Ingredients:")

    # loop through possible ingredient fields
    for i in range(1, 21):

        ingredient = meal.get(f"strIngredient{i}", "")
        measure = meal.get(f"strMeasure{i}", "")

        if ingredient and ingredient.strip():

            print(f"    {i:2}. {measure.strip():15} {ingredient.strip()}")

    # display instructions neatly
    instructions = meal.get("strInstructions", "N/A")

    print("\n  Instructions:")

    words = instructions.split()
    line = "    "

    for word in words:

        if len(line) + len(word) + 1 > 74:
            print(line)
            line = "    " + word + " "

        else:
            line += word + " "

    if line.strip():
        print(line)


# display list and allow user to select one recipe
def pick_from_list(meals, conn):

    if not meals:
        print("  No results to display.")
        return

    display_meal_list(meals)

    print(f"\n  Enter a number (1-{len(meals)}) to view full details, or 0 to go back:")

    user_choice = input("  > ").strip()

    # validate numeric input
    if not user_choice.isdigit():
        print("  Invalid input.")
        return

    selected_index = int(user_choice)

    if selected_index == 0:
        return

    if not (1 <= selected_index <= len(meals)):
        print("  Number out of range.")
        return

    selected_meal_id = meals[selected_index - 1].get("idMeal")

    send_message(conn, {
        "option": "details",
        "param": selected_meal_id
    })

    response = recv_message(conn)

    if response and response.get("status") == "ok":

        display_meal_details(response["data"])

    else:

        error_message = response.get("message") if response else "No response"
        print(f"  ERROR! {error_message}")


# -------------------------------------------------------------------
# REFERENCE MENU
# -------------------------------------------------------------------

def reference_menu(conn):

    while True:

        print_header("REFERENCE MENU")

        print("  [1] List all categories")
        print("  [2] List all areas")
        print("  [3] List all ingredients")
        print("  [4] Back to main menu")

        choice = input("\n  Select an option: ").strip()

        if choice == "1":

            send_message(conn, {
                "option": "categories",
                "param": ""
            })

            response = recv_message(conn)

            if response and response.get("status") == "ok":

                print_header("ALL CATEGORIES")

                for index, item in enumerate(response["data"], start=1):

                    category_name = item.get("strCategory", "N/A")

                    print(f"  {index:2}. {category_name}")

            else:

                error_message = response.get("message") if response else "No response"
                print(f"  ERROR! {error_message}")

        elif choice == "2":

            send_message(conn, {
                "option": "areas",
                "param": ""
            })

            response = recv_message(conn)

            if response and response.get("status") == "ok":

                print_header("ALL AREAS / CUISINES")

                for index, item in enumerate(response["data"], start=1):

                    area_name = item.get("strArea", "N/A")

                    print(f"  {index:2}. {area_name}")

            else:

                error_message = response.get("message") if response else "No response"
                print(f"  ERROR! {error_message}")

        elif choice == "3":

            send_message(conn, {
                "option": "ingredients",
                "param": ""
            })

            response = recv_message(conn)

            if response and response.get("status") == "ok":

                print_header("INGREDIENTS (first 50)")

                for index, item in enumerate(response["data"], start=1):

                    ingredient_name = item.get("strIngredient", "N/A")

                    print(f"  {index:2}. {ingredient_name}")

            else:

                error_message = response.get("message") if response else "No response"
                print(f"  ERROR! {error_message}")

        elif choice == "4":

            return

        else:

            print("  Invalid option. Please try again.")


# -------------------------------------------------------------------
# RECIPES MENU
# -------------------------------------------------------------------

def recipes_menu(conn):

    while True:

        print_header("RECIPES MENU")

        print("  [1] Search by name")
        print("  [2] Filter by category")
        print("  [3] Filter by area")
        print("  [4] Filter by ingredient")
        print("  [5] Random recipe")
        print("  [6] Back to main menu")

        choice = input("\n  Select an option: ").strip()

        # search by recipe name
        if choice == "1":

            keyword = input("  Enter the recipe name keyword:) ").strip()

            if not keyword:
                print("  Keyword cannot be empty.")
                continue

            send_message(conn, {
                "option": "search",
                "param": keyword
            })

            response = recv_message(conn)

            if response and response.get("status") == "ok":

                pick_from_list(response["data"], conn)

            else:

                print(f"  ERROR! {response.get('message') if response else 'No response'}")

        elif choice == "2":

            print(f"  Valid categories: {', '.join(sorted(VALID_CATEGORIES))}")

            category = input("  Enter category:) ").strip().capitalize()

            if category not in VALID_CATEGORIES:

                print(f"  Invalid category. Choose from: {', '.join(sorted(VALID_CATEGORIES))}")
                continue

            send_message(conn, {
                "option": "filter_category",
                "param": category
            })

            response = recv_message(conn)

            if response and response.get("status") == "ok":

                pick_from_list(response["data"], conn)

            else:

                print(f"  ERROR! {response.get('message') if response else 'No response'}")

        elif choice == "3":

            print(f"  Valid areas: {', '.join(sorted(VALID_AREAS))}")

            area = input("  Enter area/cuisine: ").strip().capitalize()

            if area not in VALID_AREAS:

                print(f"  Invalid area. Choose from: {', '.join(sorted(VALID_AREAS))}")
                continue

            send_message(conn, {
                "option": "filter_area",
                "param": area
            })

            response = recv_message(conn)

            if response and response.get("status") == "ok":

                pick_from_list(response["data"], conn)

            else:

                print(f"  ERROR! {response.get('message') if response else 'No response'}")

        elif choice == "4":

            ingredient = input("  Enter ingredient: ").strip()

            if not ingredient:
                print("  Ingredient cannot be empty.")
                continue

            ingredient = ingredient.replace(" ", "_")

            send_message(conn, {
                "option": "filter_ingredient",
                "param": ingredient
            })

            response = recv_message(conn)

            if response and response.get("status") == "ok":

                pick_from_list(response["data"], conn)

            else:

                print(f"  ERROR! {response.get('message') if response else 'No response'}")

        elif choice == "5":

            send_message(conn, {
                "option": "random",
                "param": ""
            })

            response = recv_message(conn)

            if response and response.get("status") == "ok":

                display_meal_details(response["data"])

            else:

                print(f"  ERROR! {response.get('message') if response else 'No response'}")

        elif choice == "6":

            return

        else:

            print("  Invalid option. Please try again:(")


# -------------------------------------------------------------------
# MAIN MENU
# -------------------------------------------------------------------

def main_menu(conn):

    while True:

        print_header("MAIN MENU")

        print("  [1] Browse recipes")
        print("  [2] Reference lists")
        print("  [3] Quit")

        choice = input("\n  Select an option: ").strip()

        if choice == "1":

            recipes_menu(conn)

        elif choice == "2":

            reference_menu(conn)

        elif choice == "3":

            send_message(conn, {
                "option": "quit",
                "param": ""
            })

            response = recv_message(conn)

            message = response.get("message") if response else "Disconnected."

            print(f"\n  {message}")

            return

        else:

            print("  Invalid option. Please try again:(")


# -------------------------------------------------------------------
# MAIN FUNCTION
# -------------------------------------------------------------------

def main():

    print(SEPARATOR)
    print("  Welcome to the Recipe Discovery System :)")
    print(SEPARATOR)

    # get username
    username = input("  Enter your name:) ").strip()

    if not username:
        username = "Guest"

    # connect to server
    try:

        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        conn.connect((HOST, PORT))

        print(f"  Connected to server at {HOST}:{PORT}")

    except ConnectionRefusedError:

        print(f"  ERROR! Cannot connect to {HOST}:{PORT}. Is the server running?")
        return

    # handshake with server
    send_message(conn, {"name": username})

    response = recv_message(conn)

    if response and response.get("status") == "ok":

        print(f"\n  {response.get('message', 'Connected!')}")

    else:

        print("  ERROR! Unexpected server response during handshake.")

        conn.close()

        return

    # start menu system
    try:

        main_menu(conn)

    except KeyboardInterrupt:

        print("\n  Interrupted. Closing ...")

    finally:

        conn.close()

        print("  Connection closed. Goodbye!")


if __name__ == "__main__":
    main()
