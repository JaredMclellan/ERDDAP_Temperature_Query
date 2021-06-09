ERDDAP Sea Surface Temperature Reporter

This project was made to get a collection of datasets from CKAN and ERDDAP and produce temperature reports based on the data.
Specifications based on what was listed here: https://docs.google.com/document/d/1RL7t9oqxNvFqxMVjF4QAR9wbspt8uANcK3P-6AGE3To/edit

IMPORTANT
Dependencies for this program exist. Please run setup.bat to ensure they are installed or install the packages in requirement.txt in another manner
The build folder also contains a standalone executable if issues arise.


Main.py
The main class is reponsible for the flow of the program and uses the CKAN and ERDDAP modules to accomplish this task.
It holds the important specification variables for running the script, so any minor changes to things like organization name, start date, end date, etc.
	can be made here instead of searching through the other two modules. 
	(An exception being the CIOOS server address, but I figure that part would at least remain constant)
The Main script is also responsible for plotting the data. Which is currently creates as scatter plots
I wasn't sure exactly what format to plot the data, but figured changing those details would take little work to change if needed.

CKAN.py
The CKAN module contains methods for accessing CKAN and also parsing the response provided by the CKAN API. 
These methods probably could've been included in the main script, but I found it cleaner and easier to follow in their own script.

ERDDAP.py
The ERDDAP module is responsible for both calling ERDDAP and managing the datasets provided by it.
It uses the erddapy package to accomplish most of its tasks, primarily the one pertaining to generating the RESTful URL requests.

Improvements
While considerations were made for flexibility in methods and object, there is still some rigidness in the code, particularly in the main script.
Furthermore, some of the exception checking, throwing, and handling could be improved upon. Especially if this were a program to be used with other datasets.
Also some of my comments were just created and left as is. 
For an actual project I might focus a bit more on clarity and conciseness instead of leaving it to train-of-thought style writing.

Also potential for expanding the scope of the project and using configuration files or user inputs to specify dates, variable names, datasets, etc. 
If this were an actual project this would've been an important consideration. 
However, these specifications involved running the same inputs continuously so less focus was placed on implementing any of these features.

(Also thanks for providing me with this opportunity! I realize this must've taken extra time to create and I really appreciate giving me the chance!)
