"""
--Naim Sen--

Apr 19

Handles unpacking and analysing eye tracking data

Copyright © 2019, Naim Sen
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>
"""
#%% [markdown]
# # Eye tracking analysis
# This script handles the unpacking of data from eye tracking for analysis.
# First, we load the data into a pandas dataframe from the excel sheet.
#%%
import numpy as np
import pandas as pd

#from aptipy.analysis import utilities

filepath = r"D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S8\MPhys_s8\all_participants_onlyfixations.xlsx"
results_df = pd.read_excel(filepath)
results_df.head(10)
#%% [markdown]
# # clean the data of useless columns etc.
#%%
# print out columns
results_df.columns.values
#%%
results_df = results_df.drop([
    'ExportDate', 'StudioVersionRec', 'StudioProjectName',
    'RecordingResolution', 'FixationFilter'
],
                             axis=1)
# Rename columns
results_df.rename(
    columns={
        'FixationPointX (MCSpx)': 'FixationPointX',
        'FixationPointY (MCSpx)': 'FixationPointY',
        'GazePointX (MCSpx)': 'GazePointX',
        'GazePointY (MCSpx)': 'GazePointY'
    },
    inplace=True)
results_df.head(10)

#%% [markdown]
# # Data refactoring
# We now need to create containers for each image and its associated calibration.
# First, we relabel the calibration MediaName and add an additional column (bool) to indicate
# that the data points are calibration points.
#%%
# Add new column to distinguish datapoints and calibration points
results_df['ElementType'] = np.full(len(results_df), 'DataPoint')
#%%
prev_name = results_df['MediaName'][0]
# Loop over each element
for i in range(len(results_df)):
    # ignore first element
    if i == 0:
        pass
    else:
        current_name = results_df['MediaName'][i]
        # check if the current element is the same stimulus as previous data point
        if current_name == prev_name:
            pass
        # check if current element is a calibration point
        elif current_name == 'drift_calibration.png':
            results_df['MediaName'][i] = prev_name
            results_df['ElementType'][i] = 'CalibrationPoint'
        # current element must be for a new stimulus if it is not a calibration
        # point or same as old stimulus
        else:
            prev_name = current_name

#%%
results_df

#%% [markdown]
# Next, we split the dataframe into individual dataframes for each stimulus.

#%%
dict_of_stimuli = {key: val for key, val in results_df.groupby('MediaName')}

#%% [markdown]
# ## Now split by recording...
# We want a dict of dicts of dicts
#   - {MediaName : dict{...
#        - RecordingName : dict{...
#           - ElementType : dataframe(by elementtype, by recording, by medianame) }
#               }
#            }

#%%
# Empty parent-level dictionary
dicts_of_results = dict()
# loop over dictionary of MediaName : dataframes
for stim, stim_df in dict_of_stimuli.items():
    # create daughter-level dictionary
    daughter_vals = {key: val for key, val in stim_df.groupby('RecordingName')}
    for rec, rec_df in daughter_vals.items():
        # create granddaughter-level dictionary
        gdaughter_vals = {
            key: val
            for key, val in rec_df.groupby('ElementType')
        }
        daughter_vals[rec] = gdaughter_vals
    dicts_of_results[stim] = daughter_vals

#%% [markdown]
# ## To outline the data structure...
#%%
dicts_of_results.keys()

#%%
dicts_of_results['DiegoCosta.jpg'].keys()

#%%
dicts_of_results['DiegoCosta.jpg']['Rec 01'].keys()

#%% [markdown]
# ## Handling systematic and random error
# To handle these, we look at the CalibrationPoints. Let's plot one of these...

#%%
import matplotlib.pyplot as plt

example_df = dicts_of_results['getty button.jpg']['Rec 04']['CalibrationPoint']
example_df.plot.scatter(
    'FixationPointX',
    'FixationPointY',
)
plt.xlim(0, 1366)
plt.ylim(0, 768)

example_df

#%% [markdown]
# ## Calculating systematic drift
# For each image and each recording instance, we calculate the weighted mean
# of the calibration data and take the weighted standard deviation.

#%%
from aptipy.analysis.utilities import wavg, wvar
mean_x = wavg(example_df, 'FixationPointX', 'GazeEventDuration')
mean_y = wavg(example_df, 'FixationPointY', 'GazeEventDuration')

var_x = wvar(example_df, 'FixationPointX', 'GazeEventDuration')
var_y = wvar(example_df, 'FixationPointY', 'GazeEventDuration')

plt.errorbar(
    int(mean_x),
    int(mean_y),
    xerr=np.sqrt(var_x),
    yerr=np.sqrt(var_y),
    fmt='x')
plt.xlim(0, 1366)
plt.ylim(0, 768)