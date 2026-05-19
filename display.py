# display.py
# Functions for displaying responses
# Display recipe list

def display_recipe_list(data):

    print("\n========== RECIPES ==========")
    meals = data.get("meals", []) 

    if not meals:
        print("No recipes found.")
        return

for meal in meals:

        print(f"Meal ID: {meal.get('idMeal')}")
        print(f"Recipe Name: {meal.get('strMeal')}")
        print(f"Thumbnail: {meal.get('strMealThumb')}")
        print("------------------------------")

# Display full recipe details
def display_recipe_details(data):

    print("\n========== RECIPE DETAILS ==========")

    meal = data.get("meal", {})

    if not meal:
        print("Recipe details not found.")
        return

    print(f"Name: {meal.get('strMeal')}")
    print(f"Category: {meal.get('strCategory')}")
    print(f"Area: {meal.get('strArea')}")
    print(f"Tags: {meal.get('strTags')}")


