.. _exercises:
UrbanFootprint Exercises
========================

.. _exercises_datacreation:
Data Creation
-------------

Setup:
______
Assumptions:
++++++++++++
You have access to ArcGIS

Downloads:
++++++++++

Download the zipped FileGeodatabase and BuiltTable.py to a folder on your computer, and extract the file geodatabase so that you have both the file geodatabase and the python file in the same folder. The file geodatabase will look like a folder with a .dgb extension.

FileGeodatabase (Download)
BuiltTable.py (Download)
OptionalMaterials (Download)

Using IDLE:
___________

IDLE is an Integrated Development Environment (IDE) for Python. It is installed automatically as part of the Python installation that is part of every recent ArcGIS desktop installation. 

IDLE is not a particularly fully featured IDE, nor is it my favorite. Alternate IDEs that you might consider using for your own work  include: Eclipse (with the PyDev extension), Spyder, PyCharm, WingIDE. However since those are likely to require installation with adminiatrative access, this exercise will be designed around the use of IDLE. 

Open IDLE 
Windows 7: Using the start menu,  All Programs-->ArcGIS-->Python2.7-->IDLE(Python GUI)
Wintows 8: Push the windows button to view the tiles, and then type in "idle" 

The Python shell should appear, make sure that that at the top it says something like:
::
  Python 2.7.5 (default, May 15 2013, 22:44:16) [MSC v.1500 64 bit (AMD64)] on win32

The exact version of may differ depending on the version of ArcGIS that is installed, but it should be version 2.7.X

Using the File menu on the Python shell, open the BuildTable.py file. It should open in another window.

In the shell, select Debug-->Debugger. Another window will open, this is the debugger.

In the BuildTable.py window, you can right click on any line of code and select "Set Breakpoint" to create a point where your code will pause when you're running it (called a breakpoint). 

The debugger has the following main options:

* **Go:** This button will have the code run until it gets to the next breakpoint, encounters an error, or finishes the script.
* **Step:** This button will run the currently highlighted line of code, if that line of code is a function call, it will step into that function. You don't want to use this very often in ArcPy based scripts unless yo've written your own functions.
* **Over:** Over will run the currently highlighted line of code, but if the line is a function call, it will execute the function without stepping into it.
* **Out:** If you are in a function, Out will complete the function fully and then pause when it's done. 
* **Quit:** This will stop the code execution.

When viewing the code you can push F5 to run the code. If the debugger window is active, it will start in a "Paused mode" and when you click Go it will run to your first breakpoint.

Starting Data:
______________

The file geodatabase contains the following tables and feature classes (a table that contains spatial information).

* lu_freq: a table that will let us translate from the "local land use code" into the name of the UrbanFootprint placetypes or building types that will be used to display it.
* pt_ratios: a table that contains a large number of fields that will allow us to disaggregate the starting data into subcategories. This process is the bulk of the work. The table contains one row for each place type or building type listed in lu_freq.
* yolo_start_step1: This feature class is the starting point for all of the spatial data and contains the acreages and square footages of each parcel, as well as the local land use code, and an estimate of the population, dwelling unit, and employment counts for that parcel. 
* public_yolo_county_base_feature_polygon: (feature class) Is a model of what we're trying to recreate.
* yolo_county_census_block_rates: Is a feature class with potentially useful data with rates of demographic data types assembled by census block with significant cleanup done by Calthorpe that is an example of a potential datasource for a more complex data construction process. 
