import arcpy

arcpy.env.workspace = './final_project.gdb/cs50_project'

# The defined variables will be used and defined while running code, others variables contain the features' name which
# has existed in the `final_project` database and are frequently is used while running the program. Furthermore, a list
# of global or read-only variables also exists here, the value of each variable starts with an underscore, which is used
# to keep the temporary features' name.
CALLS = "_calls"
OBS_CALLS = "_obs_calls"
CALLS_COUNT = "_calls_count"
CALLS_HOTSPOT = "_calls_hotspot"
GWR_911_CALLS = '_gwr_911_calls'
OBS_DATA_911_CALLS = "ObsData911Calls"
VISUALIZE_SURFACE_CALLS = "_visualize_surface_calls"


# The pre-launch tasks have consisted of the operation that at first gives reassurance about removing the old features
# that were used in the last try. The temporary features are removed, and a copy of the original `calls` data is
# created. Eventually, the process of integrating the features is executed.
def initialization():
    remove_old_features()
    copy_calls_feature()
    integrate_calls_in_30_feet()


# Removes the old features that were created in the last run, the name of each feature starts with an underscore.
def remove_old_features():
    for features_name in [CALLS, CALLS_COUNT, CALLS_HOTSPOT, OBS_CALLS, OBS_DATA_911_CALLS, GWR_911_CALLS]:
        arcpy.Delete_management(features_name)


# To keep the original `calls` feature, a version of that is copied into a new feature for use while run.
def copy_calls_feature():
    in_feature = "calls"
    out_feature = CALLS
    arcpy.CopyFeatures_management(in_feature, out_feature)


# Integrates features in the range of 30 feet, every feature within this range will be located in the same coordinate.
def integrate_calls_in_30_feet():
    in_feature = CALLS
    x_y_tolerance = "30 feet"
    arcpy.Integrate_management(in_feature, x_y_tolerance)


# The process is contained, a single point `feature` for each location in the dataset. Additionally, has a count field
#  reflects the number of found points.
def collect_events_into_calls_count():
    in_feature = CALLS
    out_feature = CALLS_COUNT
    arcpy.CollectEvents_stats(in_feature, out_feature)


# The result of the Hot Spot function is a new feature that is symbolized based on whether
# it is part of a statistically significant hot spot, a statistically significant
# cold spot, or is not part of any statistically significant cluster
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


# The regression analysis gives an ability to understand the factors behind observed spatial patterns. In addition,
# it can determine a better understanding of some factors contributing related to high `calls` volumes.
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


# Checks whether the residuals exhibit a random spatial pattern using the Spatial `Autocorrelation` function.
def measures_obs_calls_autocorrelation():
    in_feature = OBS_CALLS
    in_field = "StdResid"
    report_type = "GENERATE_REPORT"
    conceptualization = "Inverse Distance"
    distance_method = "EUCLIDEAN DISTANCE"
    standardization = "ROW"
    arcpy.SpatialAutocorrelation_stats(in_feature, in_field, report_type, conceptualization, distance_method,
                                       standardization)


# According to the `ordinary_obs_calls_regression` function, it should be improved in model results by moving to
# Geographically Weighted Regression. Because relationships between some or the entire explanatory variables and
# dependent variables are non-stationary. The GWR default output is a map of model residuals is showed how the
# relationship between each explanatory variable and the dependent variable is changed across the study area.
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
    initialization()
    collect_events_into_calls_count()
    create_calls_hotspot_stats()
    idw_neighbour_to_calls()
    ordinary_obs_calls_regression()
    measures_obs_calls_autocorrelation()
    geographically_regression_obs_calls()


if __name__ == "__main__":
    main()
