# Analysis 911 Responses

This project demonstrates how regression analysis is created as an ArcGIS project and contains an explanation of each step.

## Variables

The defined variables' means will be used and defined while running code, others variables contain the features' name
which has existed in the `final_project` database and are frequently is used. Furthermore, a list of global or read-only
variables also exists here, the value of each variable starts with an underscore which is used to keep the temporary
features' name.

```
CALLS = "_calls"
OBS_CALLS = "_obs_calls"
CALLS_COUNT = "_calls_count"
CALLS_HOTSPOT = "_calls_hotspot"
GWR_911_CALLS = '_gwr_911_calls'
OBS_DATA_911_CALLS = "ObsData911Calls"
VISUALIZE_SURFACE_CALLS = "_visualize_surface_calls"
```

## Initialization

The pre-launch tasks have consisted of the operation that at first gives reassurance about removing the old features
that were used in the last try. The temporary features are removed, and a copy of the original `calls` data is created.
Eventually, the process of integrating the features is executed.

- Removes the old features that were created in the last run, the name of each feature starts with an underscore.
- To keep the original `calls` feature, a version of that is copied into a new feature for use while run.
- Integrate features in the range of 30 feet, every feature within this range will be located in the same coordinate.

## Collect Events

The process is contained, a single point `feature` for each location in the dataset. Additionally, has a count field
reflects the number of found points.

## Hotspot process

The result of the `hotspot` function is a new feature that is symbolized based on whether it is part of a statistically
significant hotspot, a statistically significant `cold-spot`, or not.

## Visualise Surface

Makes the `raster` images based on a created hotspot. This output is only used in the case of the preview, not
furthermore.

## Ordinary Regression

The regression analysis gives an ability to understand the factors behind observed spatial patterns. In addition, it can
determine a better understanding of some factors contributing related to high `calls` volumes.

## Measure Autocorrelation

Checks whether the residuals exhibit a random spatial pattern using the Spatial `Autocorrelation` function.

## Geographically Regression

According to the `ordinary_obs_calls_regression` function, it should be improved in model results by moving to
Geographically Weighted Regression. Because relationships between some or the entire explanatory variables and dependent
variables are non-stationary. The GWR default output is a map of model residuals is showed how the relationship between
each explanatory variable and the dependent variable is changed across the study area.
