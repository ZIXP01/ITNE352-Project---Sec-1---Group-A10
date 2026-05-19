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
 
