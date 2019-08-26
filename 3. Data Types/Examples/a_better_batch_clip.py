import os
import arcpy


### A Better Batch clip example: #####

# From the arcpy.Clip_analysis docstring:
"""
Clip_analysis(in_features, clip_features, out_feature_class, {cluster_tolerance})
 Extracts input features that overlay the clip features.
Use this tool to cut out a piece of one feature class using one or more of the features
in another feature class as a cookie cutter. This is particularly useful for creating a new
feature class-also referred to as study area or area of interest (AOI)-that contains a
geographic subset of the features in another, larger feature class.

     * INPUTS:
      in_features (Feature Layer): The features to be clipped.
      clip_features (Feature Layer): The features used to clip the input features.
      cluster_tolerance {Linear unit}: The minimum distance separating all feature coordinates as well as the distance a coordinate can move in X or Y (or both).

     * OUTPUTS:
      out_feature_class (Feature Class): The feature class to be created.
"""

# Recall from the batch_clip.py example, we need to:


# * Decide on an output location - geodatabase (or folder for shapefiles)
# * Get the full path and feature class names of the inputs
# * Drop the extensions from the feature class names 
# * Add the .shp extension (if outputting shapefiles)
# * Replace any spaces with underscores
# * Join our output location path with the cleaned-up feature class name to get the output paths

# * Construct a data structure with the input path and output path for our clips

# * Loop over the data structure and execute the clip for each input and output

# Since we are doing that process redundantly, its a good candidate for a function.

# Let's define a function that takes an output location (workspace - either gdb or folder)
# and an input feature class and returns a properly formatted output path.


def get_output_path(workspace, input_feature_class_path):
    """
    Take a workspace and a feauture class or feature layer and return 
    a properly formatted output path
    """
    # Get the feature class name (still has the extension, if any)
    fc_name_with_ext = os.path.basename(input_feature_class_path)
    # Drop the extension (if any)
    fc_name = os.path.splitext(fc_name_with_ext)[0]
    # Replace spaces with underscores
    fc_name = fc_name.replace(' ', '_')

    # Add .shp exension if outputting shapefiles
    if not workspace.endswith('.gdb'):  # use the endswith() to check for gdb
        # If not a geodatabse, We are outputting shapefiles
        fc_name = fc_name + '.shp'

    # Join the output workspace and the clean feature class name
    output_feature_class_path = os.path.join(workspace, fc_name)    

    # return the final output path
    return output_feature_class_path


# New we can clip these corporate feature layers:
veg_data  = r'\\blm\dfs\loc\EGIS\ReferenceState\CO\CorporateData\vegetation\Colorado GAP ReGAP 2004.lyr'
geo_data  = r'\\blm\dfs\loc\EGIS\ReferenceState\CO\CorporateData\geoscience\USGS Statewide Geology.lyr'
soil_data = r'\\blm\dfs\loc\EGIS\ReferenceState\CO\CorporateData\soils\NRCS STATSGO Soils.lyr'

# By this boundary:
clip_data = r'\\blm\dfs\loc\EGIS\CO\GIS\gisuser\rgfo\mtroyer\Python_Demo\Batch_Clip\Batch_Clip.gdb\Clip_Area'

# And dump it all here:
output_gdb = r'\\blm\dfs\loc\EGIS\CO\GIS\gisuser\rgfo\mtroyer\Python_Demo\Batch_Clip\Batch_Clip.gdb'

# Grouo the inputs into a list
input_fcs = [veg_data, geo_data, soil_data]

for input_fc in input_fcs:
    output_path = get_output_path(output_gdb, input_fc)
    arcpy.Clip_analysis(in_features=input_fc, clip_features=clip_data, out_feature_class=output_path)

