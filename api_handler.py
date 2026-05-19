# api_handler.py

import requests

# Base URL for TheMealDB API
BASE_URL = "https://www.themealdb.com/api/json/v1/1/"


# Search meals by name
def search_by_name(keyword):
    url = BASE_URL + f"search.php?s={keyword}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Return meals list
        return data.get("meals", [])

    return []


# Filter meals by category
def filter_by_category(category):
    url = BASE_URL + f"filter.php?c={category}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        return data.get("meals", [])

    return []


# Filter meals by area
def filter_by_area(area):
    url = BASE_URL + f"filter.php?a={area}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        return data.get("meals", [])

    return []


# Filter meals by ingredient
def filter_by_ingredient(ingredient):
    url = BASE_URL + f"filter.php?i={ingredient}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        return data.get("meals", [])

    return []


# Get random recipe
def random_recipe():
    url = BASE_URL + "random.php"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        return data.get("meals", [])

    return []


# Get full meal details using meal ID
def lookup_by_id(meal_id):
    url = BASE_URL + f"lookup.php?i={meal_id}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        return data.get("meals", [])

    return []