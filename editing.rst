Scenario Editing
================

Goals
-----

#. To provide you with an understanding of how UrbanFootprint defines and manages place types and land use
#. To enable you to assist in defining a scenario’s targets.
#. To give you the technical skills to edit a scenario

 #. Through “painting” place types
 #. Using the query editor

Map Structure
-------------

Image here (Base + Change)

UrbanFootprint builds a scenario by adding the “change” or “increment” that you’ve painted on top of a base conditions dataset. The combination of the two produces what is known as the “End state.” The “End State” represents what will be on the ground in the future (at what ever time you’re targeting). 

Image here (Base + Change = End State)

It is important to note that this isn’t just a simple addition or replacement of the base condition with the change map. UrbanFootprint implements rules that play several roles to control how overlaps are handled.

*Infill/Redevelopment:* As you add changes you are also defining for those changes whether any overlaps with the base condition should be treated as Infill where much of the existing land use is left in place, and additional development is added to fill in any available capacity. Alternately the existing condition can be cleared from the parcel to represent a full reconstruction of the location. 

*Development Constraints:* Layers can be added to the scenario that constrain development in locations that overlap. More on these later.

How Place Types Work
--------------------

Buildings
_________

Image here (building overlaps)

We know specific details about the buildings
* Square footage
* Stories
* Parking
* Site Layout
* Energy Use
* Water Use
* Rents
* Construction Costs
In many cases we can point to a “real” building.

Image here (building editor)

Discussion
++++++++++

#. A “Building” represents a real world building that does, or could exist in the real world. It includes a significant amount of detail about the building. 
#. All of this detail remains attached to the building as it becomes a contributor to the building type and the place type. This allows us to step backwards from a place or building type to get at these details when we need to.

Building Types
______________

Image here (building group)

We can group similar buildings together to create a “Building Type”

Each building is assigned a percentage that it makes up of the building type.
Examples:
* Mid-rise Office
* Garden Apartment
* Single Family Dwelling
* Big Box Store

Image here (building type editor)

Discussion
++++++++++

#. Building types are groupings of buildings. 
#. Each building that contributes to a building type is assigned a percentage which represents its contribution to the building type.
#. The percentage is percentage of land area occupied by that building as a portion of the building type. i.e. if you had 100 acres of the building type, building A might represent 25 acres if it has a 25% representation.

Place Type
__________

Image Here (grouped building types).

A “Place Type” is a mixture of building types.

Each building type is assigned a percentage that represents it’s proportion of the Place Type’s land area.

Through assembling Place Types in this fashion we can aggregate all of the information about the buildings up to the Place Type

Image here (building type editor)

Discussion
++++++++++

#. Similarly to the relationship between buildings and building types, building types are grouped together to create place types. 
#. Each building type has a percentage that it represents of the Place Type.
#. Having built a place type, we know information about all of the buildings in it based on the relationship from place type to building type to buildings.

RUCS Types
__________

Image here (RUCS type editor)

* A parallel structure has been developed to handle the Rural Urban Connections Strategy types
* Crop, Crop Type, and Landscape Type
* These are used for Agricultural analysis

Discussion
++++++++++

The RUCS types of Crop, Crop Type, and Landscape type are a parallel structure to the building, building type, and place type structure. It’s just intended to represent the agricultural, and in the future other openspace values for analytical purposes.

Recommended Practices
_____________________

* Prepare your building types and place types prior to beginning scenario editing. 
* There are several example type sets in use to use as a starting point
* Then avoid changing them unless it becomes clear that there is an unmet need or error within a type.

Discussion
++++++++++

Changing place types mid-process can create confusion and require that you revisit previously completed work. This could be time consuming and may lead to unintended results in your scenario.


Scenario Definition
-------------------

What are the Scenario's Goals?
______________________________

When viewed regionally, what should the scenario include?
* How much population growth?
* What changes in demographics?
* What kinds of housing will accommodate them?
* How many new jobs? And what kind of job are they?
* Where will housing and job development be prioritized?
* What areas will be protected?

Discussion
++++++++++

1. Outreach and stakeholder involvement could be highly beneficial depending on your work plan
2. Many features of the scenario should be outlined at this point:

 #. Population change
 #. Employment growth 
 #. Urban Form goals (i.e. will it involve TODs, and where, what densities, walkablity?)

3.  This is a critical step. Defining the scenarios’ goals and properties sets the rest of the planning process up.

 #. Growth centers
 #. Housing types and densities
 #. Land and resource protection goals
 #. Transportation system goals

Translating the Goals into Targets
__________________________________

Translating the Goals into Targets:
* Population
* Jobs/Housing
* Housing Types/Mixes
* Jobs Types/Mixes
* Infill
* Redevelopment

Discussion
++++++++++
Define your scenario’s goals in numeric terms.
Translate the higher level goals into numeric targets that you can meet though editing the scenario’s land use.

Existing Conditions
___________________

What are the conditions on the ground now? We will need work from a detailed map of what is the reality on the ground based on:
* A Survey of Existing Conditions
* Housing Stock
* Employment Space
* Vacant Space
* Redevelopment Potential
* Transportation Infrastructure
* Other Infrastructure

Discussion
++++++++++

The existing condition matters. You will be determining what changes to apply on top of the existing conditions and how those changes will effect the existing built form.

You will get to choose whether you are adding new development while leaving the existing structures in place, or will be redeveloping the parcels through tearing down the buildings and replacing them with all new ones.

How Will the Area Change?
_________________________

Priority Locations:
 * *For Development*

  * City or Community Centers
  * Transit Corridors

 * *For Protection*

  * Agriculture
  * Recreation
  * Public Safety
  * Open Space
  * Species
  * Ecosystem Services

Discussion
++++++++++
How will you choose where to locate the changes? 

Will you be focusing on infill? 

How much greenfield development will be permitted? 

What are the priorities for protection?

Connecting to UrbanFootprint
----------------------------

Image here (log on screen)

#. Open a web browser
#. Type in the URL or click on a provided link

 #. This may either be a domain name  

 * http://Urbanfootprint.ucdavis.edu/demosite (not an active link)

 2. Or an IP address 

 * http://127.0.0.1 (not active link)

3. Enter user name and password (for demo sites)

 * Username: test 
 * Password: test

Tour of UrbanFootprint
----------------------

A basic tour of UrbanFootprint


Overview
________

Image here

Scenario Managment
__________________

Image here

Layer Management
________________

Image here

Charts
______

Image here

Map
___

Image here

Scenario Builder and Analysis
_____________________________

Image here

Scenario Mangment
-----------------

Content here


Charts
------

Content here


Layer Management
----------------

Content here

Basic Layer Management
______________________

Content here

Layer Ordering
______________

Content here

Advanced Layer Management
_________________________

Content here

Note:
You can also export layers to an ESRI File Geodatabase for use in ArcGIS. 

Manage Layere Window
____________________

Content here








