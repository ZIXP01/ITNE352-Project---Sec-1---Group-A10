import requests
import json
class ReferenceCache:
def __init__(self):
 """  Store reference lists in memory """
self.categories = []
self.areas = []
self.ingredients = []
