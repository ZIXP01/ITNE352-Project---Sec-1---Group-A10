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
