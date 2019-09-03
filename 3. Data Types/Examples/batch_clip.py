import os
import arcpy


arcpy.env.overwriteOutput = True

def deleteInMemory():
    """
    Delete in memory tables and feature classes.
    Reset to original worksapce when done.
    """
    # get the original workspace location
    orig_workspace = arcpy.env.workspace
    # Set the workspace to in_memory
    arcpy.env.workspace = "in_memory"
    # Delete all in memory feature classes
    for fc in arcpy.ListFeatureClasses():
        arcpy.Delete_management(fc)
    # Delete all in memory tables
    for tbl in arcpy.ListTables():
        arcpy.Delete_management(tbl)
    # Reset the workspace
    arcpy.env.workspace = orig_workspace


#### Batch clip example: #####
# Let's batch clip and output some features!

# Let's clip these corporate feature layers:
veg_data  = r'\\blm\dfs\loc\EGIS\ReferenceState\CO\CorporateData\vegetation\Colorado GAP ReGAP 2004.lyr'
geo_data  = r'\\blm\dfs\loc\EGIS\ReferenceState\CO\CorporateData\geoscience\USGS Statewide Geology.lyr'
soil_data = r'\\blm\dfs\loc\EGIS\ReferenceState\CO\CorporateData\soils\NRCS STATSGO Soils.lyr'

# By this boundary:
# You'll need to choose your own clip features and change this path.
clip_data = r'<CHANGE THIS: PATH TO YOUR CLIP BOUNDARY FEATURE CLASS>'


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


# To batch clip these features, we need a data strucutre that includes, for each operation:
# * a string path to the input features to clip (full file path or TOC feature layer name),
# * a string path to a the clip features (full file path or TOC feature layer name),
# * a full file path to the output feature class (must be a full file path to a geodatabase feature class or shapefile)
# We will disregard the optional cluster_tolerance paramter in this example.

# Importantly, the clip features will be the same (clip_data variable above) in each case, so we really only
# need to worry about the in_features path and the out_feature_class path.

# We'll output everything to a common location (geodatabase or folder)

# Choose your own geodatabase and change this path.
# If you want to output shapefiles, you'll need to change this path to a folder location.
output_gdb = r'<CHANGE THIS: PATH TO YOUR GEODATABASE>'

# We may as well reuse the input (in_features) names for our outputs so it is clear what each output is..
# So, we need to first extract the feature class names from the inputs.
# Use os.path.basename()
veg_feature_class_name_with_ext = os.path.basename(veg_data)
geo_feature_class_name_with_ext = os.path.basename(geo_data)
soil_feature_class_name_with_ext = os.path.basename(soil_data)

# Keep in mind that the output will be a feature class and not a feature layer (as in the input, in this example)
# Thus, don't forget to remove the .lyr extension from your feature class name.
# Use os.path.splitext()
# os.path.splitext returns a container (tuple) of the file/filepath without the extension, and the extension itself. 
# The file/filepath is in index positon [0], and the extension is index [1].

# Keep in mind:
# if you are outputting geodatabase feature classes, you don't need to add an output extension to your output path.
# However, if you are outputting shapefiles, you'll need to add the .shp extension to your output paths
output_veg_data_name = os.path.splitext(veg_feature_class_name_with_ext)[0]  # Note the indexing [0] to get the first item in the tuple
output_geo_data_name = os.path.splitext(geo_feature_class_name_with_ext)[0]
output_soil_data_name = os.path.splitext(soil_feature_class_name_with_ext)[0]
# For shapefiles:
# e.g. output_veg_data_name = os.path.splitext(veg_feature_class_name_with_ext)[0] + '.shp'

# While we have the output names handy, we should address the issue that these layers have spaces in the file names.
# That is invalid for feature class names, so we need to replace the spaces with underscores.
# Strings have a .replace method (function) that takes two parameters - character(s) to replace, character(s) to replace with 
# We can re-assign values to the same variable name as well.
output_veg_data_name = output_veg_data_name.replace(' ', '_')
output_geo_data_name = output_geo_data_name.replace(' ', '_')
output_soil_data_name = output_soil_data_name.replace(' ', '_')

# Now that we have the output feature class names, we need to construct our full file path with the gdb path.
# Use os.path.join() 
# os.path.join takes a list of strings and joins them into a single path:

output_veg_data_path = os.path.join(output_gdb, output_veg_data_name)
output_geo_data_path = os.path.join(output_gdb, output_geo_data_name)
output_soil_data_path = os.path.join(output_gdb, output_soil_data_name)

# Now that we have our input and output paths, we can build our data structure.
# The simple solution is to use a list of lists (or list of tuples):

clip_operations = [  # This is a list
   [veg_data, output_veg_data_path],  # These are also lists, nested within the outer list
   [geo_data, output_geo_data_path],
   [soil_data, output_soil_data_path], 
]

# We are ready to batch execute:
# We need to take each sublist in the clip_operations list, one at a time, and hand off the 
# first element as the in_features and the second element as the out_features_class.
# we can use a for/in loop:


for sublist in clip_operations:
    in_data = sublist[0]  # Get the first element
    out_path = sublist[1]  # Get the second element
    # The actual function - at last!
    # We will use the clip features (clip_data) from above - because it is the same in all cases
    # We can pass the paramters by position - i.e. Clip_analysis(in_features, clip_features, out_feature_class)
    # Or by keyword:
    arcpy.Clip_analysis(in_features=in_data, clip_features=clip_data, out_feature_class=out_path)
    deleteInMemory()   