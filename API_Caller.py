# This module does all the API lifting
import json
import requests

# Searches CKAN for some specified criteria
# If more time, refine the API search to target the specific field (organization.name), but for now this returns the data needed
def search_Ckan(search):
    response = requests.get("https://cioosatlantic.ca/ckan/api/3/action/package_search?q=" + search)
    results = response.json()["result"]["results"]
    return results