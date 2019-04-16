"""
--Naim Sen--
--Toby Ticehurst--

Apr 19

Handles unpacking and analysing eye tracking data

Copyright © 2018, Naim Sen
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

filepath = r"D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S8\MPhys_s8\all_participants_onlyfixations.xlsx"
results_dframe = pd.read_excel(filepath)
print(results_dframe.head(10))
#%% [markdown]
# Now clean the data of useless columns etc.
#%%
# print out columns
print(results_dframe.columns.values)
#%%
results_dframe = results_dframe.drop([
    'ExportDate', 'StudioVersionRec', 'StudioProjectName',
    'RecordingResolution', 'FixationFilter'
],
                                     axis=1)
print(results_dframe.head(10))

#%% [markdown]
# # Data restructuring
# We now need to create containers for each image and its associated calibration.
# First, we relabel the calibration MediaName and add an additional column (bool) to indicate
# that the data points are calibration points.
#%%
# Add new column
results_dframe['IsCalibration'] = np.full(len(results_dframe), False)
#%%
prev_name = results_dframe['MediaName'][0]
# Loop over each element
for i in range(len(results_dframe)):
    # ignore first element
    if i == 0:
        pass
    else:
        current_name = results_dframe['MediaName'][i]
        # check if the current element is the same stimulus as previous data point
        if current_name == prev_name:
            pass
        # check if current element is a calibration point
        elif current_name == 'drift_calibration.png':
            results_dframe['MediaName'][i] = prev_name
            results_dframe['IsCalibration'][i] = True
        # current element must be for a new stimulus if it is not a calibration
        # point or same as old stimulus
        else:
            prev_name = current_name

results_dframe

#%%
