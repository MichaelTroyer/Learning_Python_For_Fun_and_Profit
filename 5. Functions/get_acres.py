import arcpy
import csv


def gordon_cant_count_so_he_needs_a_python_function(path_to_fc, acres_field_name='Acres', csv_path=None):
    '''
    Look for an acres field, add if not found, update acres field, return total acres.
    
    Parameters:
    * path_to_fc: path to a feature class (must be a polygon)
    * acres_field_name: name of field to look for or create if not found.

    Return:
    * Total acres (float)
    '''

    # List fields in feature class
    fields = arcpy.ListFields(path_to_fc)

    field_names = []
    for field in fields:
        field_name = field.name
        field_names.append(field_name)

    #field_names = [field.name for field in arcpy.ListFields(path_to_fc)]

    # Look for acres field, create if not found
    if not acres_field_name in field_names:
        print 'Adding field'
        arcpy.AddField_management(path_to_fc, acres_field_name, "DOUBLE")

    # Update acres
    print 'Updating acres'
    arcpy.CalculateField_management(path_to_fc, acres_field_name, "!shape.area@ACRES!", "PYTHON_9.3")

    acres_total = 0
    with arcpy.da.SearchCursor(path_to_fc, acres_field_name) as cur:
        for row in cur:
            acres_total = acres_total + float(row[0])

    # acres_total = sum([float(row[0]) for row in arcpy.da.SearchCursor(path_to_fc, acres_field_name)])

    print 'Total acres: ' + str(acres_total)
    return acres_total


feature_class = r'T:\CO\GIS\gisuser\rgfo\mtroyer\Python_Demo\Demo.gdb\Demo'

gordon_cant_count_so_he_needs_a_python_function(feature_class, 'Test_Acres')