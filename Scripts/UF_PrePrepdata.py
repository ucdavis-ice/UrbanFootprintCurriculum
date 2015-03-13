'''
Example of data preparation for UrbanFootprint. This script extracts values
from an existing base parcel dataset that has been converted into a file
geodatabase.

More information on UrbanFootprint is available at:
http://urbanfootprintcurriculum.readthedocs.org/
http://www.calthorpe.com/scenario_modeling_tools


Copyright (C) 2015  Nathaniel roth

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    http://www.gnu.org/copyleft/gpl.html

'''
# Import libraries
import arcpy
import datetime

# Functions
def Message(msg):
    '''
    Print a message with a timestamp
    '''
    print("|".join([str(datetime.datetime.now()),msg]))

# Paths and dataset names
fgdbpath = r"M:\UrbanFootprintCurriculumData\YoloData.gdb"
fcname  = "yolo_start_canad83"
outtable = r"M:\UrbanFootprintCurriculumData\YoloData.gdb\pt_ratios"

# Prepare a codeblock for the field calculator
codeblock = """def DivideField(a,b):
    if b == None:
        return 0
    elif b == 0:
        return 0
    else:
        return a/b """

# Set arcpy envronments
arcpy.env.workspace = fgdbpath
arcpy.env.overwriteOutput = True



stats = []
# list of fields to calulate statistics on.
sumlist = ['acres_developable','sqft_parcel','pop','hh','du','emp_retail_services','emp_restaurant','emp_accommodation',
           'emp_arts_entertainment','emp_other_services','emp_office_services','emp_public_admin','emp_education',
           'emp_medical_services','emp_manufacturing','emp_wholesale','emp_transport_warehousing','emp_utilities',
           'emp_construction','emp_agriculture','emp_extraction','bldg_sqft_detsf_sl','bldg_sqft_detsf_ll','bldg_sqft_attsf','bldg_sqft_mf',
           'bldg_sqft_retail_services','bldg_sqft_restaurant','bldg_sqft_accommodation','bldg_sqft_arts_entertainment','bldg_sqft_other_services',
           'bldg_sqft_office_services','bldg_sqft_public_admin','bldg_sqft_education','bldg_sqft_medical_services','bldg_sqft_transport_warehousing',
           'bldg_sqft_wholesale','acres_parcel_res','acres_parcel_emp','acres_parcel_mixed_use','acres_parcel_no_use',
           'acres_parcel_res_detsf','acres_parcel_res_detsf_sl','acres_parcel_res_detsf_ll','acres_parcel_res_attsf',
           'acres_parcel_res_mf','acres_parcel_emp_ret','acres_parcel_emp_off','acres_parcel_emp_pub','acres_parcel_emp_ind','acres_parcel_emp_ag',
           'acres_parcel_emp_military','residential_irrigated_sqft','commercial_irrigated_sqft','du_detsf','du_attsf','du_mf','du_detsf_ll','du_detsf_sl','du_mf2to4','du_mf5p' ]

# Build the list that runs the SUM of each fo fthe fields
for sc in sumlist:
    stats.append([sc,'SUM'])
# Calculate the sum of each column grouped by the built_form_key
Message("Starting Summary Stats")
arcpy.Statistics_analysis('yolo_start_canad83', outtable, stats, 'built_form_key')
Message("Finished Summary Stats")

Message("Adding and Calculating total emp")
arcpy.AddField_management(outtable, 'tot_emp', 'DOUBLE')
expr = "!SUM_emp_retail_services! + !SUM_emp_restaurant! + !SUM_emp_accommodation! + !SUM_emp_arts_entertainment! + !SUM_emp_other_services! + !SUM_emp_office_services! + !SUM_emp_public_admin! + !SUM_emp_education! + !SUM_emp_medical_services! + !SUM_emp_manufacturing! + !SUM_emp_wholesale! + !SUM_emp_transport_warehousing! + !SUM_emp_utilities! + !SUM_emp_construction! + !SUM_emp_agriculture! + !SUM_emp_extraction!"
arcpy.CalculateField_management(outtable, 'tot_emp',expr, "PYTHON_9.3")
Message("total_emp done")

# Calculate Average Employment Percents
empfields = ['emp_retail_services','emp_restaurant','emp_accommodation','emp_arts_entertainment','emp_other_services',
             'emp_office_services','emp_public_admin','emp_education','emp_medical_services','emp_manufacturing',
             'emp_wholesale','emp_transport_warehousing','emp_utilities','emp_construction','emp_agriculture','emp_extraction']

Message('Processing Emp Fields')
for ef in empfields:
    Message("Working on: {ef}".format(ef = ef))
    newfield = "_".join(['pct',ef])
    arcpy.AddField_management(outtable, newfield, 'DOUBLE')
    expr = "DivideField(!SUM_{ef}!,!tot_emp!)".format(ef=ef)
    arcpy.CalculateField_management(outtable, newfield,expr, "PYTHON_9.3",codeblock)
Message('Processed Emp Fields')  
   
# Calculate Average Dwelling Unit Percents
dufields = ['du_detsf','du_attsf','du_mf']
Message('Processing du Fields')
for ef in dufields:
    Message("Working on: {ef}".format(ef = ef))
    newfield = "_".join(['pct',ef])
    arcpy.AddField_management(outtable, newfield, 'DOUBLE')
    expr = "DivideField(!SUM_{ef}!,!SUM_du!)".format(ef=ef)
    arcpy.CalculateField_management(outtable, newfield,expr, "PYTHON_9.3", codeblock)
Message('Processed du Fields')  

Message('Handling specifis for du subtypes')
newfield = "_".join(['pct','du_detsf_ll'])
arcpy.AddField_management(outtable, newfield, 'DOUBLE')
expr = "DivideField(!SUM_du_detsf_ll!,!SUM_du!)"
arcpy.CalculateField_management(outtable, newfield,expr, "PYTHON_9.3",codeblock) 
newfield = "_".join(['pct','du_detsf_sl'])
arcpy.AddField_management(outtable, newfield, 'DOUBLE')
expr = "DivideField(!SUM_du_detsf_sl!,!SUM_du!)"
arcpy.CalculateField_management(outtable, newfield,expr, "PYTHON_9.3",codeblock) 
newfield = "_".join(['pct','du_mf2to4'])
arcpy.AddField_management(outtable, newfield, 'DOUBLE')
expr = "DivideField(!SUM_du_mf2to4!,!SUM_du!)"
arcpy.CalculateField_management(outtable, newfield,expr, "PYTHON_9.3",codeblock) 
newfield = "_".join(['pct','du_mf5p'])
arcpy.AddField_management(outtable, newfield, 'DOUBLE')
expr = "DivideField(!SUM_du_mf5p!,!SUM_du!)"
arcpy.CalculateField_management(outtable, newfield,expr, "PYTHON_9.3",codeblock) 
    

# Calculate the Average Acres   
Message('Processing Acres')
acrefields = ['acres_parcel_res','acres_parcel_res_detsf','acres_parcel_res_detsf_sl','acres_parcel_res_detsf_ll','acres_parcel_res_attsf',
           'acres_parcel_res_mf','acres_parcel_emp','acres_parcel_mixed_use','acres_parcel_no_use','acres_parcel_emp_ret','acres_parcel_emp_off','acres_parcel_emp_pub','acres_parcel_emp_ind',
           'acres_parcel_emp_ag','acres_parcel_emp_military']

for af in acrefields:
    Message("Working on: {af}".format(af = af))
    newfield = "_".join(['pct',af])
    arcpy.AddField_management(outtable, newfield, 'DOUBLE')
    #arcpy.CalculateField_management(outtable, newfield,0, "PYTHON_9.3")
    expr = "DivideField(!SUM_{af}!,!SUM_acres_developable!)".format(af=af)
    arcpy.CalculateField_management(outtable, newfield,expr, "PYTHON_9.3",codeblock)
Message('Processed Acres')

Message('Processing bldg square feet')
bldfields = ['bldg_sqft_detsf_sl','bldg_sqft_detsf_ll','bldg_sqft_attsf','bldg_sqft_mf',
           'bldg_sqft_retail_services','bldg_sqft_restaurant','bldg_sqft_accommodation','bldg_sqft_arts_entertainment','bldg_sqft_other_services',
           'bldg_sqft_office_services','bldg_sqft_public_admin','bldg_sqft_education','bldg_sqft_medical_services','bldg_sqft_transport_warehousing',
           'bldg_sqft_wholesale']

for af in bldfields:
    Message("Working on: {af}".format(af = af))
    newfield = "_".join(['sqftratio',af])
    arcpy.AddField_management(outtable, newfield, 'DOUBLE')
    #arcpy.CalculateField_management(outtable, newfield,0, "PYTHON_9.3")
    expr = "DivideField(!SUM_{af}!,!SUM_sqft_parcel!)".format(af=af)
    arcpy.CalculateField_management(outtable, newfield,expr, "PYTHON_9.3",codeblock)

Message('Processed bldg square feet')


Message("Processing irrigated space")

bldfields = ['residential_irrigated_sqft','commercial_irrigated_sqft']

for af in bldfields:
    Message("Working on: {af}".format(af = af))
    newfield = "_".join(['sqftratio',af])
    arcpy.AddField_management(outtable, newfield, 'DOUBLE')
    #arcpy.CalculateField_management(outtable, newfield,0, "PYTHON_9.3")
    expr = "DivideField(!SUM_{af}!,!SUM_sqft_parcel!)".format(af=af)
    arcpy.CalculateField_management(outtable, newfield,expr, "PYTHON_9.3",codeblock)

Message("Processed irrigated space")

Message("Process HH")
arcpy.AddField_management(outtable, "hh_per_du", 'DOUBLE')
#arcpy.CalculateField_management(outtable, "hh_per_du",0, "PYTHON_9.3")
expr = "DivideField(!SUM_hh!,!SUM_du!)"
arcpy.CalculateField_management(outtable, "hh_per_du",expr, "PYTHON_9.3",codeblock)
Message("Processed HH")

Message("Process pop")
arcpy.AddField_management(outtable, "pop_per_hh", 'DOUBLE')
#arcpy.CalculateField_management(outtable, "pop_per_hh",0, "PYTHON_9.3")
expr = "DivideField(!SUM_pop!,!SUM_hh!)"
arcpy.CalculateField_management(outtable, "pop_per_hh",expr, "PYTHON_9.3",codeblock)
Message("Processed pop")

Message("Done")


