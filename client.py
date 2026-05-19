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
