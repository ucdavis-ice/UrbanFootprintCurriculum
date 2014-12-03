Data Preparation
================

Goals
-----

* Provide an overview of data needed by UrbanFootprint
* Describe the required fields for base data
* Walk through the steps used for SACOG’s base data preparation.
* Work through an example of preparing data for a county.

Data Needs
----------

UrbanFootprint is a data intensive application. The effort that goes into data collection, preparation, and review should not be underestimated.

The base data which is also called the base canvas, or existing conditions dataset will require extensive data collection, processing, and then review prior to its use. The requirements imposed by UrbanFootprint on its base conditions data include strict adherence to the data schema, and the need for a detailed understanding of the existing conditions at a parcel level. If you are working in a geographic area that has not had a prior installation of UrbanFootprint, it is unlikely that there will be a dataset that you can use without substantial effort in createing a base condition dataset.

Scenario development has looser data requirements, but will require that you have an understanding of regional and local plans for the future, and have planned out goals for the scenario that can be translated onto a map at a parcel scale. 

Environmental constraint layers influence the intensity of development that is possible in locations where these constraints are present. 

Reference layers provide a visual reference to UrbanFootprint users while editing or visualizing scenarios.

The transportation module (and any other modules that build on its results) will require that you have substantial additional data derived from both regional transportation infrastructure GIS as well as a travel demand model.

Some of the other analytical modules also require climate data to run.


Data Types and Sources
----------------------

Data for the Base Canvas
________________________

.. csv-table:: **Base Canvas**
	:header: Data Type, Potential Source, Notes
	:widths: 50, 50, 50
	:file: OtherDocs/basecanvas.csv

Data for Scenario Development
_____________________________

.. csv-table:: **Scenario Development**
	:header: Data Type, Potential Source, Notes
	:widths: 50, 50, 50
	:file: OtherDocs/scenariodevelopment.csv

Environmental Constraints
_________________________

.. csv-table:: **Environmental Constraints/Climate Resilience**
	:header: Data Type, Potential Source, Notes
	:widths: 50, 50, 50
	:file: OtherDocs/environmentalconstraints.csv

Base Reference Layers
_____________________

.. csv-table:: **Reference Layers**
	:header: Data Type, Potential Source, Notes
	:widths: 50, 50, 50
	:file: OtherDocs/referencedata.csv

Transportation Data
___________________

.. csv-table:: **Transportation**
	:header: Data Type, Potential Source, Notes
	:widths: 50, 50, 50
	:file: OtherDocs/transportation.csv

Analysis Reference Data
_______________________

.. csv-table:: **Analysis Reference Data**
	:header: Data Type, Potential Source, Notes
	:widths: 50, 50, 50
	:file: OtherDocs/analysisreference.csv



Base Data Schema: SACOG
-----------------------

* The structure and field names are critical.
* There is a single table
* Which will be uploaded to PostGIS
* For convenience the discussion of fields will be divided into groups

 * Metadata and Geography
 * Paint Configuration
 * Parcel Areas/Types
 * Residential/Housing
 * Employment
 * Building Square footage
 * Outdoor Irrigated Area

Metadata and Geography
______________________

.. csv-table:: **Metadata and Geography**
	:header: Field Name, Description
	:widths: 25, 75
	:file: OtherDocs/metadatageog.csv

Paint Configuration
___________________

These fields are not used in the base features dataset, but are included to maintain an identical structure to the End State data.

.. csv-table:: **Paint Configuration**
	:header: Field Name, Description
	:widths: 25, 75
	:file: OtherDocs/paintconfig.csv


Parcel Area/Type
________________

.. csv-table:: **Parcel Area/Type**
	:header: Field Name, Description
	:widths: 25, 75
	:file: OtherDocs/parcelareatype.csv


Residential and Housing
_______________________

.. csv-table:: **Residential and Housing**
	:header: Field Name, Description
	:widths: 25, 75
	:file: OtherDocs/residential.csv

Employment
__________

.. csv-table:: **Employment**
	:header: Field Name, Description
	:widths: 25, 75
	:file: OtherDocs/employment.csv

Building Square Footage
_______________________

.. csv-table:: **Building Square Footage**
	:header: Field Name, Description
	:widths: 25, 75
	:file: OtherDocs/buildinginfo.csv

Outdoor Irrigated Area
______________________

.. csv-table:: **Outdoor Irrigated Area**
	:header: Field Name, Description
	:widths: 25, 75
	:file: OtherDocs/irrigated.csv

Base Data Preparation: SACOG
----------------------------

Input Data
__________

.. image:: graphics/GenericPic1.png
	:align: right
	:width: 300 px

* SACOG parcel data

 * SACOG Land Use 
 * Dwelling Units

* SACOG TAZ
* Census 2010 Blockgroups
* Census 2010 Tracts

Data Preparation: Topology
__________________________

.. image:: graphics/ExistingConditions_smalll.png
	:align: left
	:width: 300 px

* Parcels must not overlap
* Clip the dataset to the county border
* Remove roads and waterbodies

Dwelling Units
______________

.. csv-table:: **Residential Land Use Crosswalk**
	:header: SACOG Use Code, Dwelling Unit Type
	:widths: 25, 75
	:file: OtherDocs/lu_crosswalk.csv

* Total DU = SACOG Parcel DU
* Controlled to TAZ totals
* Assign DU type using crosswalk (right), and assign DU totals to du_detsf
* Du_detsf_sl and du_detsf_ll based on sf/du calculation.
* ACS rates for Attached SF, MF 2-4, and MF 5 plus are applied to all parcels with MF units

Households
__________

.. image:: graphics/ExistingConditions_smalll.png
	:width: 300 px

* HH from SACOG 2008
* DU from Parcel Data
* Occupancy rate = HH/DU

Population
__________

* Calculate Average HH by block group from census data
* Ave. HH size = pop/hh
* Then multiply the HH count in each parcel by the Ave. HH size.

Employment
__________

* Parcel employment from SACOG 2008
* Crosswalk using the table 
* Use LEHD to disaggregate where needed. (next page)
* Accommodation extracted using SACOG Employment Inventory

.. csv-table:: **Employment Land Use Crosswalk**
	:header: SACOG Use Code, Employment Type
	:widths: 25, 75
	:file: OtherDocs/emp_crosswalk.csv

Employment Processing and Source
________________________________

.. csv-table:: **Employment Processing and Source**
	:header: UF Employment Sub Category, Method for Spatially Deriving Field at Parcel, SACSIM Category
	:widths: 25, 75, 75
	:file: OtherDocs/emp_processing.csv

Disaggregation
______________

* This technique is used several times during data preparation.
* Calculate the proportion of each SACOG category that goes into each UF Employment Category.
* Use the LEHD 2010 near imputed rate datase as the basis for the disaggregation. 

i.e. %emp_entrec = 100*emp_entrec/
(emp_entrec+emp_other_services+emp_accomodation)


Dataset 1 (higher accuracy): 95 employees

Dataset 2: 50 retail, 30 service, and 20 industrial employees.

+---------+------+------+------+------+------+-----+
|Total Emp|Ret. %|Ser. %|Ind. %|# Ret.|# Ser.|# Ind|
+=========+======+======+======+======+======+=====+
|95       |50	 |30	|20    |47.5  |28.5  |19   |
+---------+------+------+------+------+------+-----+


Concerns: Zeros and Nulls

Building Square Footage
_______________________

Need info

Irrigated Square Footage
________________________

Need info

Developablity
_____________

Need info

Alternate Method: SANDAG
------------------------

* Base Schema

 * Expanded compared to SACOG
 * Includes HH income
 * Population Educational Attainment

* Data Sources

 * 2012 parcels, have DU and land use
 * 2012 EDD employment points with 2-4 digit NAICS codes
 * MGRA with Pop (by gender and age), and Households by income category
 * ACS Data (5 year block group and 1 year PUMS)

Loading Base Data into UrbanFootprint
-------------------------------------

#. Upload via ftp
#. Create new geographic area in Django
#. Create new schema in database
#. Load data to schema

Keep the Goal in Mind
---------------------

* Data for your region will be unique
* This process should serve as a starting point for developing your data, not a fixed recipe.

Exercise
--------

* Download XXXX
* And unzip it into a folder.
* Inside the folder here will be a mxd and folders with data and scripts
* We’re going to step through the scripts. 
