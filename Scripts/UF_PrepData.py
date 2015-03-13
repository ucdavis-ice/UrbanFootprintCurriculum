'''
Example of data preparation for UrbanFootprint. This script adds and calculates
most of the mandatory fields for a base dataset. Note that this is a signficant
simplification from what you would probably want to do in a production
deployment of UrbanFootprint.

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

# Import needed libraries
import os, sys
import arcpy
import datetime
import time

# Functions
def Message(msg):
    '''
    Print a message with a timestamp
    '''
    print("|".join([str(datetime.datetime.now()),msg]))

# Input Parameters
fgdbpath = r"YoloData.gdb" # the path to the file geodatabase that should have come with this script. This may need to be edited to point to the right place. 
step1 = "yolo_start" # the starting feature class name
step2 = "step2" # the next sets are simple names that we'll use for saving our work at various points in the process
step3 = "step3"
step4 = "step4"
step5 = "step5"
step6 = "step6"
bltform = "lu_freq" # the table name with the land use frequence data that'll let us link to the built_form_key variable
srctable = r"pt_ratios" # ratios and percentages for each place type were calculated into this table. It joins in on built_form_key.
ldctable = r"ldc_and_int_density" # ratios and percentages for each place type were calculated into this table. It joins in on built_form_key.

# Attribute fields to include in the output. 
AddFields = [[u'geography_id', u'Integer', 4, 0, 0], 
          [u'source_id', u'String', 80, 0, 0], 
          [u'region_lu_code', u'String', 80, 0, 0], 
          [u'built_form_key', u'String', 80, 0, 0],
          [u'acres_developable', u'Double', 8, 0, 0], 
          [u'developable_proportion', u'Double', 8, 0, 0], 
          [u'land_development_category', u'String', 80, 0, 0], 
          [u'intersection_density_sqmi', u'Double', 8, 0, 0], 
          [u'sqft_parcel', u'Double', 8, 0, 0], 
          [u'acres_gross', u'Double', 8, 0, 0], 
          [u'acres_parcel', u'Double', 8, 0, 0], 
          [u'acres_parcel_res', u'Double', 8, 0, 0], 
          [u'acres_parcel_emp', u'Double', 8, 0, 0], 
          [u'acres_parcel_mixed_use', u'Double', 8, 0, 0], 
          [u'acres_parcel_no_use', u'Double', 8, 0, 0], 
          [u'pop', u'Double', 8, 0, 0], 
          [u'hh', u'Double', 8, 0, 0], 
          [u'du', u'Double', 8, 0, 0], 
          [u'du_detsf', u'Double', 8, 0, 0], 
          [u'du_attsf', u'Double', 8, 0, 0], 
          [u'du_mf', u'Double', 8, 0, 0], 
          [u'emp', u'Double', 8, 0, 0], 
          [u'emp_ret', u'Double', 8, 0, 0], 
          [u'emp_off', u'Double', 8, 0, 0], 
          [u'emp_pub', u'Double', 8, 0, 0], 
          [u'emp_ind', u'Double', 8, 0, 0], 
          [u'emp_ag', u'Double', 8, 0, 0], 
          [u'emp_military', u'Double', 8, 0, 0], 
          [u'du_detsf_ll', u'Double', 8, 0, 0], 
          [u'du_detsf_sl', u'Double', 8, 0, 0], 
          [u'du_mf2to4', u'Double', 8, 0, 0], 
          [u'du_mf5p', u'Double', 8, 0, 0], 
          [u'emp_retail_services', u'Double', 8, 0, 0], 
          [u'emp_restaurant', u'Double', 8, 0, 0], 
          [u'emp_accommodation', u'Double', 8, 0, 0], 
          [u'emp_arts_entertainment', u'Double', 8, 0, 0], 
          [u'emp_other_services', u'Double', 8, 0, 0], 
          [u'emp_office_services', u'Double', 8, 0, 0], 
          [u'emp_public_admin', u'Double', 8, 0, 0], 
          [u'emp_education', u'Double', 8, 0, 0], 
          [u'emp_medical_services', u'Double', 8, 0, 0], 
          [u'emp_manufacturing', u'Double', 8, 0, 0], 
          [u'emp_wholesale', u'Double', 8, 0, 0], 
          [u'emp_transport_warehousing', u'Double', 8, 0, 0], 
          [u'emp_utilities', u'Double', 8, 0, 0], 
          [u'emp_construction', u'Double', 8, 0, 0],
          [u'emp_agriculture', u'Double', 8, 0, 0], 
          [u'emp_extraction', u'Double', 8, 0, 0], 
          [u'bldg_sqft_detsf_sl', u'Double', 8, 0, 0], 
          [u'bldg_sqft_detsf_ll', u'Double', 8, 0, 0], 
          [u'bldg_sqft_attsf', u'Double', 8, 0, 0], 
          [u'bldg_sqft_mf', u'Double', 8, 0, 0], 
          [u'bldg_sqft_retail_services', u'Double', 8, 0, 0], 
          [u'bldg_sqft_restaurant', u'Double', 8, 0, 0], 
          [u'bldg_sqft_accommodation', u'Double', 8, 0, 0], 
          [u'bldg_sqft_arts_entertainment', u'Double', 8, 0, 0], 
          [u'bldg_sqft_other_services', u'Double', 8, 0, 0], 
          [u'bldg_sqft_office_services', u'Double', 8, 0, 0], 
          [u'bldg_sqft_public_admin', u'Double', 8, 0, 0], 
          [u'bldg_sqft_education', u'Double', 8, 0, 0], 
          [u'bldg_sqft_medical_services', u'Double', 8, 0, 0], 
          [u'bldg_sqft_transport_warehousing', u'Double', 8, 0, 0], 
          [u'bldg_sqft_wholesale', u'Double', 8, 0, 0], 
          [u'acres_parcel_res_detsf', u'Double', 8, 0, 0], 
          [u'acres_parcel_res_detsf_sl', u'Double', 8, 0, 0], 
          [u'acres_parcel_res_detsf_ll', u'Double', 8, 0, 0], 
          [u'acres_parcel_res_attsf', u'Double', 8, 0, 0], 
          [u'acres_parcel_res_mf', u'Double', 8, 0, 0], 
          [u'acres_parcel_emp_ret', u'Double', 8, 0, 0], 
          [u'acres_parcel_emp_off', u'Double', 8, 0, 0], 
          [u'acres_parcel_emp_pub', u'Double', 8, 0, 0], 
          [u'acres_parcel_emp_ind', u'Double', 8, 0, 0], 
          [u'acres_parcel_emp_ag', u'Double', 8, 0, 0], 
          [u'acres_parcel_emp_military', u'Double', 8, 0, 0], 
          [u'residential_irrigated_sqft', u'Double', 8, 0, 0], 
          [u'commercial_irrigated_sqft', u'Double', 8, 0, 0], 
          [u'created', u'Date', 8, 0, 0], 
          [u'updated', u'Date', 8, 0, 0], 
          [u'dev_pct', u'Double', 8, 0, 0], 
          [u'density_pct', u'Double', 8, 0, 0], 
          [u'gross_net_pct', u'Double', 8, 0, 0], 
          [u'dirty_flag', u'SmallInteger', 2, 0, 0] 
          ]


# Setup arcpy workspace
arcpy.env.workspace = fgdbpath
arcpy.env.overwriteOutput = True

step = 1

# Start the real work
Message("Step {step}: Make a Copy".format(step=step))
step +=1
arcpy.Copy_management(os.path.join(fgdbpath,step1), os.path.join(fgdbpath,step2))

Message("Step {step}: Joining Table".format(step=step))
step +=1
fld =  [u'built_form_key', u'String', 80, 0, 0]
arcpy.AddField_management(os.path.join(fgdbpath,step2), fld[0],fld[1],"","",fld[2])
arcpy.MakeFeatureLayer_management(os.path.join(fgdbpath,step2),'jnlayer' )
arcpy.AddJoin_management('jnlayer', 'local_lu_code', os.path.join(fgdbpath,bltform), 'region_lu_code')

Message('Step {step}: Calculate Built Form'.format(step=step))
step +=1
#Note the CalculateField_management tool is pretty slow, that's why we're going to use an update cursor for most of the rest of the work
arcpy.CalculateField_management('jnlayer','step2.built_form_key', '!lu_freq.built_form_key!',"PYTHON_9.3") 
#Then add an index so that the next join can happen more quickly.
arcpy.AddIndex_management('jnlayer','built_form_key','bltfrm')

Message("Step {step}: Joining Table".format(step=step))
step +=1
arcpy.AddJoin_management('jnlayer', 'built_form_key', os.path.join(fgdbpath,srctable), 'built_form_key')
arcpy.CopyFeatures_management('jnlayer', os.path.join(fgdbpath,step3))
arcpy.RemoveJoin_management('jnlayer',srctable)
arcpy.RemoveJoin_management('jnlayer',bltform)
arcpy.Delete_management('jnlayer')


Message("Step {step}: Removing Unneded Fields".format(step=step))
step +=1
# Delete many fields that aren't needed to save space and time on copies
# We don't any of the fields that start with 'pt_ratios_SUM'
delfields1 = arcpy.ListFields( os.path.join(fgdbpath,step3))
delfields2 = []
for fld in delfields1:
    if fld.name[0:13] == 'pt_ratios_SUM': 
        delfields2.append(fld.name)
arcpy.DeleteField_management(os.path.join(fgdbpath,step3), delfields2)
delfields1 = None
delfields2 = None


Message("Step {step}: Adding Fields".format(step=step))
step +=1
fldnames =[]
for fld in AddFields:
    fldnames.append(fld[0])
    arcpy.AddField_management(os.path.join(fgdbpath,step3), fld[0],fld[1],"","",fld[2])

Message("Step {step}: Populating Fields".format(step=step)) # Takes ~8 Minutes on my computer
step +=1
with arcpy.da.UpdateCursor(os.path.join(fgdbpath,step3),fldnames) as cursor:
    for row in cursor:
        i = 0
        for fld in AddFields:
            if fld[1] in ['Double','Integer','SmallInteger']:
                row[i] = 0
            elif fld[1] in ['String']:
                row[i] = ""
            elif fld[1] in ['Date']:
                row[i] = time.strftime("%Y/%m/%d")
            i+=1
        cursor.updateRow(row)

Message("Step {step}: Make a copy".format(step=step))
step +=1
arcpy.Copy_management(os.path.join(fgdbpath,step3), os.path.join(fgdbpath,step4))        

Message("Step {step}: Calculate Fixed Values".format(step=step))
step +=1
fields = ['step2_pcl_id', 'geography_id','source_id',
          'step2_acres','acres_developable','acres_gross','acres_parcel',
          'step2_pcl_sqft','sqft_parcel',
          'step2_dunits','du',
          'step2_emp_count','emp',
          'step2_built_form_key','built_form_key',
          'step2_local_lu_code','region_lu_code',
          'dev_pct','density_pct','gross_net_pct','dirty_flag','developable_proportion']
cursor = arcpy.da.UpdateCursor(os.path.join(fgdbpath,step4),fields)
for row in cursor:
    row[1] = row[0]
    row[2] = str(row[0])
    row[4] = round(row[3],2) # acres
    row[5] = round(row[3],2) # acres
    row[6] = round(row[3],2) # acres
    row[8] = round(row[7],2) # square feet
    row[10] = round(row[9],2) # du
    row[12] = round(row[11],2) # emp
    row[14] = row[13] # built form key
    row[16] = row[15] # regional_lu_code
    row[17] = 1.0 # dev_pct
    row[18] = 1.0 # density_pct
    row[19] = 1.0 # gross_net_pct
    row[20] = 0.0 # dirty_flag
    row[21] = 1.0 # developable_proportion
    cursor.updateRow(row)

Message("Step {step}: Calculate Populations and households".format(step=step))
step +=1
fields = ['hh','pt_ratios_hh_per_du','du',
          'pop','pt_ratios_pop_per_hh']

cursor = arcpy.da.UpdateCursor(os.path.join(fgdbpath,step4),fields)
for row in cursor:
    row[0] = round(row[1]*row[2],2) # households
    row[3] = round(row[4]*row[0],2) # pop
    cursor.updateRow(row)
    
Message("Step {step}: Calculate Acres".format(step=step))
step +=1

flds = ['acres_parcel_res','acres_parcel_emp','acres_parcel_mixed_use','acres_parcel_no_use','acres_parcel_res_detsf','acres_parcel_res_detsf_sl','acres_parcel_res_detsf_ll','acres_parcel_res_attsf',
           'acres_parcel_res_mf','acres_parcel_emp_ret','acres_parcel_emp_off','acres_parcel_emp_pub','acres_parcel_emp_ind','acres_parcel_emp_ag','acres_parcel_emp_military']
fields = ['acres_parcel']
for fld in flds:
    fields.append(fld)
    fields.append("pt_ratios_pct_{fld}".format(fld=fld))

cursor = arcpy.da.UpdateCursor(os.path.join(fgdbpath,step4),fields)
for row in cursor:
    i = 1
    for fld in flds:
        row[i] = round(row[i+1]*row[0] ,2)
        cursor.updateRow(row)
        i+=2

Message("Step {step}: Calculate Employment".format(step=step))
step +=1
flds = ['emp_retail_services','emp_restaurant','emp_accommodation','emp_arts_entertainment','emp_other_services',
             'emp_office_services','emp_public_admin','emp_education','emp_medical_services','emp_manufacturing',
             'emp_wholesale','emp_transport_warehousing','emp_utilities','emp_construction','emp_agriculture','emp_extraction']
fields = ['emp']
for fld in flds:
    fields.append(fld)
    fields.append("pt_ratios_pct_{fld}".format(fld=fld))

cursor = arcpy.da.UpdateCursor(os.path.join(fgdbpath,step4),fields)
for row in cursor:
    i = 1
    for fld in flds:
        row[i] = round(row[i+1]*row[0] ,2)
        cursor.updateRow(row)
        i+=2

Message("Step {step}: Calculate Building Square Feet".format(step=step))
step +=1
flds = ['bldg_sqft_detsf_sl','bldg_sqft_detsf_ll','bldg_sqft_attsf','bldg_sqft_mf',
           'bldg_sqft_retail_services','bldg_sqft_restaurant','bldg_sqft_accommodation','bldg_sqft_arts_entertainment','bldg_sqft_other_services',
           'bldg_sqft_office_services','bldg_sqft_public_admin','bldg_sqft_education','bldg_sqft_medical_services','bldg_sqft_transport_warehousing',
           'bldg_sqft_wholesale']
fields = ['sqft_parcel']
for fld in flds:
    fields.append(fld)
    fields.append("pt_ratios_sqftratio_{fld}".format(fld=fld))

cursor = arcpy.da.UpdateCursor(os.path.join(fgdbpath,step4),fields)
for row in cursor:
    i = 1
    for fld in flds:
        row[i] = round(row[i+1]*row[0],2)
        cursor.updateRow(row)
        i+=2

Message("Step {step}: Calculate Dwelling Units".format(step=step))
step +=1
# Primary Dwelling Unit division
flds = ['du_detsf','du_attsf','du_mf']
fields = ['du']
for fld in flds:
    fields.append(fld)
    fields.append("pt_ratios_pct_{fld}".format(fld=fld))

cursor = arcpy.da.UpdateCursor(os.path.join(fgdbpath,step4),fields)
for row in cursor:
    i = 1
    for fld in flds:
        row[i] = round(row[i+1]*row[0],2)
        cursor.updateRow(row)
        i+=2

# Detatched SF processing
flds = ['du_detsf_sl','du_detsf_ll']

fields = ['du_detsf']
for fld in flds:
    fields.append(fld)
    fields.append("pt_ratios_pct_{fld}".format(fld=fld))

cursor = arcpy.da.UpdateCursor(os.path.join(fgdbpath,step4),fields)

for row in cursor:
    i = 1
    for fld in flds:
        row[i] = round(row[i+1]*row[0],2)
        cursor.updateRow(row)
        i+=2

# Multi-family processing
flds = ['du_mf2to4','du_mf5p']

fields = ['du_mf']
for fld in flds:
    fields.append(fld)
    fields.append("pt_ratios_pct_{fld}".format(fld=fld))

cursor = arcpy.da.UpdateCursor(os.path.join(fgdbpath,step4),fields)

for row in cursor:
    i = 1
    for fld in flds:
        row[i] = round(row[i+1]*row[0],2)
        cursor.updateRow(row)
        i+=2

Message("Step {step}: Irrigated area".format(step=step))
step +=1
flds = ['residential_irrigated_sqft','commercial_irrigated_sqft']
fields = ['sqft_parcel']
for fld in flds:
    fields.append(fld)
    fields.append("pt_ratios_sqftratio_{fld}".format(fld=fld))

cursor = arcpy.da.UpdateCursor(os.path.join(fgdbpath,step4),fields)
for row in cursor:
    i = 1
    for fld in flds:
        row[i] = round(row[i+1]*row[0],2)
        cursor.updateRow(row)
        i+=2

Message("Step {step}: Make a copy".format(step=step))
step +=1
arcpy.Copy_management(os.path.join(fgdbpath,step4), os.path.join(fgdbpath,step5)) 

Message("Step {step}: Join Intersection Density and Land Development Class".format(step=step))
step +=1
arcpy.AddIndex_management(step3,'geography_id','geoid_idx')
arcpy.MakeFeatureLayer_management(os.path.join(fgdbpath,step5),'jnlayer2' )
arcpy.AddJoin_management('jnlayer2', 'geography_id', os.path.join(fgdbpath,ldctable), 'geography_id')
arcpy.CalculateField_management('jnlayer2','step5.land_development_category', '!ldc_and_int_density.land_development_category!',"PYTHON_9.3")
arcpy.CalculateField_management('jnlayer2','step5.intersection_density_sqmi', '!ldc_and_int_density.intersection_density_sqmi!',"PYTHON_9.3")
arcpy.RemoveJoin_management('jnlayer2',ldctable)

Message("Step {step}: Copy and Cleanup".format(step=step))
step +=1
arcpy.Copy_management(os.path.join(fgdbpath,step5), os.path.join(fgdbpath,step6))
delfields1 = arcpy.ListFields( os.path.join(fgdbpath,step6))
delfields2 = []
for fld in delfields1:
    if fld.name[0:9] == 'pt_ratios':
        delfields2.append(fld.name)
    elif fld.name[0:7] == 'lu_freq':
        delfields2.append(fld.name)    
    elif fld.name[0:5] == 'step2':
        delfields2.append(fld.name)
        
arcpy.DeleteField_management(os.path.join(fgdbpath,step6), delfields2)
delfields1 = None
delfields2 = None

Message("Finished")
    

