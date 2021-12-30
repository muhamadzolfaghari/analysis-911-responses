import arcpy

arcpy.env.workspace = './final_project.gdb/cs50_project'

# At here we have the list of global or const variables, the value of a variable which
# means will be used and defined while running code, others one has existed in the `final_project` database.
CALLS = "calls"
CALLS_COUNT = "calls_count"
CALLS_HOTSPOT = "calls_hotspot"
OBS_CALLS = "obs_calls"
OBS_DATA_911_CALLS = "ObsData911Calls"
VISUALIZE_SURFACE_CALLS = "visualize_surface_calls"
GWR_911_CALLS = 'gwr_911_calls'


# Removes the old features that were created in the last run, the name of each feature starts with an underscore.
def remove_old_features():
    for features_name in [CALLS, CALLS_COUNT, CALLS_HOTSPOT, OBS_CALLS, OBS_DATA_911_CALLS, GWR_911_CALLS]:
        arcpy.Delete_management(features_name)


# To keep the original `calls` feature, a version of that is copied into a new feature for use while run.
def copy_calls_feature():
    in_feature = "original_calls"
    out_feature = CALLS
    arcpy.CopyFeatures_management(in_feature, out_feature)


# Integrates features in the range of 30 feet, every feature within this range will be located in the same coordinate.
def integrate_calls_in_30_feet():
    in_feature = CALLS
    x_y_tolerance = "30 feet"
    arcpy.Integrate_management(in_feature, x_y_tolerance)


# Through the `CALLS` feature, the count's field as `ICount` is measured and added to the `CALLS_COUNT` feature.
def collect_events_into_calls_count():
    in_feature = CALLS
    out_feature = CALLS_COUNT
    arcpy.CollectEvents_stats(in_feature, out_feature)


# Based on the weight of each feature, and study on the wide range of these, approximately 99% it can be sure where is
# the exact location of hotspot and cold-spot.
def create_calls_hotspot_stats():
    in_feature = CALLS_COUNT
    input_field = "ICOUNT"
    out_feature = CALLS_HOTSPOT
    cons_spatial_rel = "Fixed Distance Band"
    distance_method = "EUCLIDEAN_DISTANCE"
    distance_threshold = 1400
    standardization = "None"
    arcpy.HotSpots_stats(in_feature, input_field, out_feature, cons_spatial_rel, distance_method, standardization,
                         distance_threshold)


# Makes the raster images based on a created hotspot. This output is only used in the case of the preview, not
# furthermore.
def idw_neighbour_to_calls():
    in_feature = CALLS_HOTSPOT
    z_value_field = "GiZScore"
    out_feature = VISUALIZE_SURFACE_CALLS
    idw = arcpy.sa.Idw(in_feature, z_value_field)
    idw.save(out_feature)


# The factors that are effective on the dependent variable are computed by regression. The factors that are determined
# by `OBS_DATA_911_CALLS` and its effect on the final changes.
def ordinary_obs_calls_regression():
    in_feature = OBS_DATA_911_CALLS
    unique_id = "UniqID"
    out_feature = OBS_CALLS
    dependent_var = "Calls"
    explanatory_vars = "Pop;Jobs;LowEduc;Dst2UrbCen"
    coefficient_out_table = "olsCoefTab.dbf"
    diagnostic_out_table = "olsDiagTab.dbf"
    arcpy.OrdinaryLeastSquares_stats(in_feature, unique_id, out_feature, dependent_var, explanatory_vars,
                                     coefficient_out_table, diagnostic_out_table)


# At this stage, the question of (Is spatial distribution of accidental exists?) is answered, and it shows that
# needs to improve the result next step, unless there are any errors the result is suitable.
# But in this case study, it is necessary to do an extra step to resolve that through a weighted regression.
def measures_obs_calls_autocorrelation():
    in_feature = OBS_CALLS
    in_field = "StdResid"
    report_type = "GENERATE_REPORT"
    conceptualization = "Inverse Distance"
    distance_method = "EUCLIDEAN DISTANCE"
    standardization = "ROW"
    arcpy.SpatialAutocorrelation_stats(in_feature, in_field, report_type, conceptualization, distance_method,
                                       standardization)


#  This regression method is used, when variables in all ranges can't predict the changes in a fixed way and remain
#  variable. To resolve that, it's necessary to use GWR regression.
def geographically_regression_obs_calls():
    in_feature = OBS_DATA_911_CALLS
    dependent_variable = "Calls"
    explanatory_variables = "Pop;Jobs;LowEduc;Dst2UrbCen"
    out_feature = GWR_911_CALLS
    kernel_type = "ADAPTIVE"
    bandwidth_method = "AICc"
    arcpy.GeographicallyWeightedRegression_stats(in_feature, dependent_variable, explanatory_variables, out_feature,
                                                 kernel_type, bandwidth_method)


def main():
    remove_old_features()
    copy_calls_feature()
    integrate_calls_in_30_feet()
    collect_events_into_calls_count()
    create_calls_hotspot_stats()
    idw_neighbour_to_calls()
    ordinary_obs_calls_regression()
    measures_obs_calls_autocorrelation()
    geographically_regression_obs_calls()


if __name__ == "__main__":
    main()
