""" This module does all the CKAN work for the challenge, from API work to formatting responses
While only the functions needed for the exercise are included in here, there's room for expansion
"""
import json
import requests

def organizationSearch(id):
    """Searches CKAN for packages based on an organization name
    Returns the results of the search request as json
    Keyword arguments:
    id -- ID of the organization as listed in CKAN
    """
    response = requests.get("https://cioosatlantic.ca/ckan/api/3/action/package_search?fq=organization:" + id)
    jsonResponse = response.json()
    return jsonResponse

def getPackageCount(response):
    """Returns the amount of packages found from a search result
    Keyword arguments:
    response -- JSON formatted response resulting from a CKAN search
    """
    count = response["result"]["count"]
    return int(count)

def getPackages(response):
    """Extracts packages from a search result and returns them as a list
    Returns a list of packages (one for each dataset found in the search)
    Keyword arguments:
    response -- JSON formatted response resulting from a CKAN search
    """
    packages = response["result"]["results"]
    return packages

def getResourceUrls(packages):
    """Extracts resource URLs from a list of packages and returns as a list
    Keyword arguments:
    packages -- List of packages (datasets) from the resulting CKAN search
    """
    urls = []
    for i in range(len(packages)):
        urls.append(packages[i]["resources"][0]["url"])
    return urls