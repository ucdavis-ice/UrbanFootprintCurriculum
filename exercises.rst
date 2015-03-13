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

Download the zipped FileGeodatabase and UF_PrepData.py to a folder on your computer, and extract the file geodatabase so that you have both the file geodatabase and the python file in the same folder. The file geodatabase will look like a folder with a .gdb extension.

* FileGeodatabase http://downloads.ice.ucdavis.edu/~neroth/uf/DataCreation.zip
* Script: :download:`UF_PrepData.py <Scripts/UF_PrepData.py>`

Optional Materials:

* http://downloads.ice.ucdavis.edu/~neroth/uf/DataCreationOptional.zip
* Optional Script: :download:`UF_PrePrepdata.py <Scripts/UF_PrePrepdata.py>`
* Optional sql: :download:`UF_DataPrepReassembly.sql <Scripts/UF_DataPrepReassembly.sql>`

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

Using the File menu on the Python shell, open the UF_PrepData.py file. It should open in another window.

In the shell, select Debug-->Debugger. Another window will open, this is the debugger.

In the UF_PrepData.py window, you can right click on any line of code and select "Set Breakpoint" to create a point where your code will pause when you're running it (called a breakpoint). 

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
* ldc_and_int_density: a table with land development class and intersection density calculated for each parcel
* yolo_start: This feature class is the starting point for all of the spatial data and contains the acreages and square footages of each parcel, as well as the local land use code, and an estimate of the population, dwelling unit, and employment counts for that parcel. 


Optional Materials:
___________________

The optional data contains some data that was used to build the inputs for the exercise, or may be interesting from a technical standpoint.
* public_yolo_county_base_feature_polygon: (feature class) Is a model of what we're trying to recreate.
* yolo_county_census_block_rates: Is a feature class with potentially useful data with rates of demographic data types assembled by census block with significant cleanup done by Calthorpe that is an example of a potential datasource for a more complex data construction process. 

Stepping Through:
_________________


This is a very simplistic approach to building a base data set. We will use assumed average values for each placetype to split a parcel data set with a "local" land use code by crosswalking the local land use code to place type, and then using estimates for each parcel of the number of dwelling units, employees, and parcel acres/square feet to prepare the input data. 


Set break points on lines 32, 38, 45, 57, 143, 149, 153, 160, 167, 176, 190, 197, 216, 245, 256, 274, 292, 311, 362, 382, 391

We'll step through the code, explaining what is going on as we go to try to develop a better idea of what data is needed for the base conditions of UrbanFootprint

This will let us break the code into manageable chunks to explain. These sections are identified based on the line that the section starts on.

**Section 1:** line 32, Imports

Import the needed libraries (collections of commands) needed to run the script. 

os and sys, are system libraries that let us work with files and paths

arcpy contains almost all of the Esri functionality for working with data.

datetime and time let us use times values.

**Section 2:** line 38, Defining a Function

This is a simple function that lets us print a message onto the screen including the time that the message was generated. It's useful for tracking how long tasks take.

**Section 3:** line 45, Parameters

Give default values to some variables that we'll be using like the path to the geodatabase.

**Section 4:** line 57, Fields

This is a list of all of the fields (except for the geometry field) and the type of data that they contain. This list will be used to add all of the needed fields to the dataset.

**Section 5:** line 143, Arcpy Workspace

Setting some defaults for Arcpy. The default workspace is taken from the value we set above, and it will allow the automatic overwriting of outputs if you rerun the script.

We're also going to make a copy of the starting point dataset so that it's easy to return if needed.

**Section 6:** line 153, Beginning the calculations

Add a field to store the built_form_key. Create a join between *yolo_start* and the built form table based on the local land use code.

**Section 7:** line 160, Calculate built_form_key

Store built_form_key (or place type) into the field we created for it. It is worth noting that the CalculateField function from Arcpy is relatively slow. However, it works a bit better across joins so I'm using it here. In most other parts of this example we'll use a faster alternate method for doing the calculations.

We'll also add an Index to the field we just calculated to make joins and calculate operations perform more quickly.

**Section 8:** line 167, Join the Source Table 

Join in the Source Table which contains our "averages" for each place type to the starting layer based on built_form_key. Then we'll copy the result to a new feature class and do a little cleanup of objects we won't need any more.

**Section 9:** line 176, Remove unneeded fields

To reduce the size of the dataset we're going to be working with a little, we remove some unneeded fields that we joined in.

**Section 10:** line 190, Add Fields

Using the list we created above, we add each of those fields to the current version of the data.

**Section 11:** line 197, Set default values

To make sure we don't end up with any null values we loop through all of the fields and add in appropriate placeholder values using an update cursor to improve our speed. This step can take quite a while and we make another copy of the data afterwards so that we can start from this point if needed.

**Section 12:** line 216, Starting to fill in values that are constant across the dataset

Using an update cursor we begin to calculate the values from our starting tables into the fields that we've created. This section contains values that are direct copies from the source data.

**Section 13:** line 245, Calculate Populations and Households

We use the average persons per households per dwelling unit, and population per household values for the place type to convert from dwelling units to (occupied) housing units (households), and to population.

**Section 14:** line 256, Calculating Acres

We apply the ratios of acres by place type to total acres to populate the acre total fields for each set of uses. This is the model for what we'll be doing for most of the following calculations.

**Section 15:** line 274, Calculate Employment.

Calculate the proportion of employees by place type that fall into each sub category.

**Section 16:** line 292, Calculate Building Square Feet

Using what is effectively a floor area ratio of the parcel square footage for each place type, calculate the acres for each building type.

**Section 17:** line 311, Dwelling Unit Calculations

First we divide the total dwelling unit count into single family detached, single family attached, and multi-family using place type averages.

Next we repeat the process to subdivide single family detached into small lot and large lot units. We also divide multi-family into 2 to 4 unit and 5 or more unit categories.

**Section 18:** line 362, Irrigated Area Calculations

Using place type average rates we calculate the irrigated square footages for commercial and residential uses.

**Section 19:** line 382, Join and Calculate the Land Development Class and Intersection Densities

Using the geography_id join the ldc_and_int_density table to our working dataset and calculate the values into the working dataset.

**Section 20:** line 391, Final Copy and Cleanup

Make a final copy of our dataset, and clean out the fields that we won't be needing.

Loading the Data:
_________________

This next step of loading this data can be technically challenging, and is going to depend on your system, so it'll only be described here, not actually completed.

First, the dataset that you've created needs to be converted into PostGIS, the easiest is to use Esri's Data Interoperability Extension to export the data into postgis. With new versions of QGIS, it is possible to read file geodatabases and export to PostGIS. Unfortunately, we have to be careful to not truncate the field names we've just been calculating.

Once the data is in PostGIS, there will be some data clean up because the translation between Esri's data types and PostGIS's is not perfect. This will include the creation of the wkb_geometry (well known binary geometry) field and making sure that none of your fields have too many decimal places for the fields they're moving into. We tried to handle that above by using the rounding functions. In general it is probably worth taking a templating approach where you use an existing dataset as a model for the new one and substitute in new data as needed.



 




