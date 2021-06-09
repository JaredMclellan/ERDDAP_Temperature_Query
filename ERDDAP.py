"""This module is involved with anything ERDDAP related
This includes making the call to the ERDDAP API
To managing the datasets provided from the request
"""
import datetime
from erddapy import ERDDAP

# Dataset class for storing information about a specific dataset
class Dataset:
    """
    A class used to represent an ERDDAP dataset
    A dataset should have an ID, URL, start time, end time
        ID is generated from the URL upon initialization
        Raw Data is collected from making an API call to ERDDAP using the above variables
    For specific methods involving variables see the child classes (in this case SSTDataset)
    """
    def __init__(self, url, startTime, endTime):
        """Takes a dataset via url, as well as start and end times for the data
        Keyword arguments:
        url -- URL of the dataset in ERRDAP
        startTime -- Starting time to bound the data
        endTime -- Ending time to bound the data
        """
        self.url = url
        self.id = getIdFromUrl(url)
        self.startTime = formatTime(startTime)
        self.endTime = formatTime(endTime)
        self.rawData= ""
    
    def __str__(self):
        """String formatting for output"""
        output = "Dataset ID: " + self.id
        output += "\nDataset URL: " + self.url
        output += "\nStart Time: " + self.startTime
        output += "\nEnd Time: " + self.endTime
        output += "\nRaw Data:\n" + self.rawData.to_string()
        return output

    def getMaximum(self, variable):
        """Gets the maximum value of a specified variable in the data
        """
        if str(self.rawData):
            allMaxs = self.rawData.max().to_dict()
            maxVal = allMaxs[variable]
        else:
            maxVal = "N/A"
        return maxVal

    def getMinimum(self, variable):
        """Gets the minimum value of a specified variable in the data
        """
        if str(self.rawData):
            allMins = self.rawData.min().to_dict()
            minVal = allMins[variable]
        else:
            minVal = "N/A"
        return minVal

    def getMean(self, variable):
        """Gets the mean value of a specified variable in the data
        """
        if str(self.rawData):
            allMeans = self.rawData.mean().to_dict()
            meanVal = allMeans[variable]
        else:
            meanVal = "N/A"
        return meanVal

    def getMedian(self, variable):
        """Gets the median value of a specified variable in the data
        """
        if str(self.rawData):
            allMedians = self.rawData.median().to_dict()
            medianVal = allMedians[variable]
        else:
            medianVal = "N/A"
        return medianVal

    def createRequest(self, variables):
        """Gets ERDDAP data from CIOOS based on the object's ID and a list of variables
        No error checking here right now, but should probably include something to catch failed requests
        Keyword arguments:
        variables -- list of variable names
        """
        e = ERDDAP(
            server = "https://cioosatlantic.ca/erddap/",
            protocol = "tabledap"
            )
        e.response = "csv"
        e.dataset_id = self.id
        e.constraints = {
            "time>=": self.startTime,
            "time<=": self.endTime
        }
        e.variables=variables
        self.rawData = e.to_pandas()

class SSTDataset(Dataset):
    """
    Child class of dataset with methods focused on working with sea surface temperature (SST)
    """
    def calculateSSTStats(self, variable):
        """Finds total statistics for sea surface temperature in ERDDAP dataframe
        Keyword arguments:
        variable -- Name of the variable to collect information for
        """
        self.sstMean = super().getMean(variable)
        self.sstMedian = super().getMedian(variable)
        self.sstMax = super().getMaximum(variable)
        self.sstMin = super().getMinimum(variable)

    def __str__(self):
        """String formatting for output"""
        output = "Dataset ID: " + self.id
        output += "\nDataset URL: " + self.url
        output += "\nStart Time: " + self.startTime
        output += "\nEnd Time: " + self.endTime
        output += "\nSST Mean: " + str(self.sstMean) + "°C"
        output += "\nSST Median: " + str(self.sstMedian) + "°C"
        output += "\nSST Maximum: " + str(self.sstMax) + "°C"
        output += "\nSST Minimum: " + str(self.sstMin) + "°C"
        return output

def formatTime(input):
    """Formats datetime into a method recognized by ERDDAP
    Keyword arguments:
    input - A datetime object to convert"""
    formatted = input.strftime("%Y-%m-%dT%H:%M:%SZ")
    return formatted


def getIdFromUrl(url):
    """Extracts an ERDDAP dataset ID from its URL
    CKAN only stores the ERDDAP URL, but the ID is useful for using with erddapy
    While not the most adaptable method, CKAN has given the links in a predictable method for this particular challenge
    Keyword Arguments:
    url -- URL of the dataset in ERDDAP
    """
    id = url.replace("https://cioosatlantic.ca/erddap/tabledap/", "").replace(".html", "")
    return id

