# display.py
# Functions for displaying responses
# Display recipe list

def display_recipe_list(data):

    print("\n========== RECIPES ==========")
    meals = data.get("meals", [])

    if not meals:
        print("No recipes found.")
        return
