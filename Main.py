#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main script responsible for the program flow
Location for variables essential for altering the output of the program such as
    organization id, start time, end time, name of the SST variable
Using organization ID, it searches CKAN for any packages matching in the search
From there it collects the ERDDAP URL from each package found and uses it to
    generate the dataset along with the start time, end time, and variable name
Then the important stats are collected for the temperature report (mean, median, max, min)
Finally a plot is created based on the raw data collected
"""

import CKAN
import ERDDAP
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

# Not 100% sure if it's temp_c or temp_water_c, but if it's the wrong one just have to change this one spot to fix
sstVarName = "temp_c"

# These might be taken as input for an actual program, but for ease of the demo these will be hard coded
startTime = datetime.datetime(2021,1,1,0,0,0)
endTime = datetime.datetime(2021,2,28,23,59,59)
organization = "cmar"
variables = ["time", sstVarName]

# Response is the JSON response to the query
response = CKAN.organizationSearch(organization)

# If no matches were found, little point running the rest of the program
count = CKAN.getPackageCount(response)
if count>0:
    # Get a list of the URLs needed to access the ERDDAP datasets
    packages = CKAN.getPackages(response)
    erddapUrls = CKAN.getResourceUrls(packages)

    # Create a file to write to based on the time of the request
    fileDir = "Reports/"
    filePrefix = "SST_" + datetime.datetime.now().strftime("%Y%m%dT%H%M%S") + "_"
    reportName = "Report.txt"
    try:
        f = open(fileDir + filePrefix + reportName, "x")
        f.close()
    except:
        print(reportName + " already exists")

    # Header for the file
    f = open(fileDir + filePrefix + reportName, "a")
    f.write("Found " + str(count) + " matches for " + organization + " in CKAN:\n\n" )
    print("Found " + str(count) + " matches for " + organization + " in CKAN:\n\n")

    # Run the ERDDAP script for each URL that was retrieved from CKAN
    for i in range(len(erddapUrls)):
        currentUrl = erddapUrls[i]
        print("Processing: " + currentUrl)
        sstData = ERDDAP.SSTDataset(currentUrl, startTime, endTime) 
        sstData.createRequest(variables)
        sstData.calculateSSTStats(sstVarName)
        f.write(str(sstData) + "\n\n")
        print(str(sstData) + "\n\n")

        # Creates scatter plot for temperature for each set of data
        # For larger data sets, might be useful to have this outside the loop so it can run continuously
        # However in this scenario, 3 plots isn't too bad to shift through
        plotData = sstData.rawData
        plotData["time (UTC)"] = pd.to_datetime(plotData["time (UTC)"], format="%Y-%m-%dT%H:%M:%SZ")
        tempPlot = plotData.plot(x = "time (UTC)", y= sstVarName, kind= "scatter", figsize = (12, 6), title= " Temperature plot for dataset " + sstData.id)
        tempPlot.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        tickGap = mdates.DayLocator(interval = 7)
        tempPlot.xaxis.set_major_locator(tickGap)
        plt.savefig(fileDir + filePrefix + "Fig_" +  str(sstData.id) + ".png")
        plt.show()
        plt.close()

    print("Finished output")
    f.close()
else:
    print("No package matches found in CKAN. Exiting")