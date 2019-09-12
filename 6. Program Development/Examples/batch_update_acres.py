import arcpy
import csv
import os


overwrite = arcpy.env.overwriteOutput
arcpy.env.overwriteOutput = True


#TODO: Check for polygons - don;t try to update point or line acres!


def get_feature_classes_from_GDB(gdb):
    """
    Return the full file path of all feature classses in gdb.
    """
    original_workspace = arcpy.env.workspace
    arcpy.env.workspace = gdb
   
    fcs = []
    for fds in arcpy.ListDatasets(feature_type='feature') + ['']:
        for fc in arcpy.ListFeatureClasses(feature_dataset=fds):
            fcs.append(os.path.join(gdb, fds, fc))             

    arcpy.env.workspace = original_workspace  
    return fcs


def update_acres(path_to_fc, acres_field_name='Acres'):
    '''
    Look for an acres field, add if not found, update acres field, return total acres.
    
    Parameters:
    * path_to_fc: path to a feature class (must be a polygon)
    * acres_field_name: name of field to look for or create if not found.

    Return:
    * Total acres
    '''

    # Check Geometry
    arcpy.CheckGeometry_management(path_to_fc, r'in_memory\check_geo_table')
    if int(arcpy.GetCount_management(r'in_memory\check_geo_table')[0]):
        arcpy.AddMessage('Error in feature class: {}'.format(path_to_fc))
        return None

    # List fields in feature class
    field_names = [field.name for field in arcpy.ListFields(path_to_fc)]

    # Look for acres field, create if not found
    if not acres_field_name in field_names:
        print 'Adding field'
        arcpy.AddField_management(path_to_fc, acres_field_name, "DOUBLE")

    # Update acres
    print 'Updating acres'
    arcpy.CalculateField_management(path_to_fc, acres_field_name, "!shape.area@ACRES!", "PYTHON_9.3")

    try:
        acres_total = sum([float(row[0]) for row in arcpy.da.SearchCursor(path_to_fc, acres_field_name)])
    except:
        acres_total = None

    print 'Total acres: ' + str(acres_total)
    return acres_total



def batch_update_acres(gdb_path, csv_path):
    
    csv_rows = []
    
    fc_paths = get_feature_classes_from_GDB(gdb_path)
    
    for fc_path in fc_paths:
        print fc_path        
        acres = update_acres(fc_path, acres_field_name='Acres_Update')
        csv_rows.append((fc_path, acres))

    print csv_rows

    with open(csv_path, 'wb') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['FC_Name', 'Acres'])

        for row in csv_rows:
            csvwriter.writerow(row)
    
    return



if __name__ == '__main__':

    gdb_path = r'T:\CO\GIS\gisuser\rgfo\mtroyer\Current Projects\crrg18037p_Mt_Shavano\CF_LM_R132.gdb'
    csv_path = r'T:\CO\GIS\gisuser\rgfo\mtroyer\Current Projects\crrg18037p_Mt_Shavano\Update_Acres.csv'

    batch_update_acres(gdb_path, csv_path)
