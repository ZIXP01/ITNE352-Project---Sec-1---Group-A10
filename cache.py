import requests
import json
class ReferenceCache:
def __init__(self):
 """  Store reference lists in memory """
self.categories = []
self.areas = []
self.ingredients = []
 # Base API URL
self.base_url = "https://www.themealdb.com/api/json/v1/1"
def load_cache(self):
 """ Load reference data from TheMealDB API """
 print("Loading reference cache...")
  self.categories = self.get_categories()
   self.areas = self.get_areas()
 self.ingredients = self.get_ingredients()
  # Save data into JSON file
  self.save_reference_file()
  print("Reference cache loaded successfully.")
 def get_categories(self):
  """ Fetch meal categories from API """
 url = f"{self.base_url}/list.php?c=list"
 try:
  response = requests.get(url)
  data = response.json()
return [item["strCategory"] for item in data["meals"]]
except Exception as error:
print(f"Error loading categories: {error}")
  return []
def get_areas(self):
 """ Fetch meal areas/cuisines from API """
 url = f"{self.base_url}/list.php?a=list"
try:
 response = requests.get(url)
  data = response.json()
return [item["strArea"] for item in data["meals"]]
except Exception as error:
print(f"Error loading areas: {error}")
 return []
def get_ingredients(self):
 """  Fetch meal ingredients from API  """
url = f"{self.base_url}/list.php?i=list"
try:
 response = requests.get(url)
