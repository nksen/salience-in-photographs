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
# Next, we split the dataframe into individual dataframes for each recording.

#%%
dict_of_recordings = {
    key: val
    for key, val in results_df.groupby('RecordingName')
}

#%% [markdown]
# ## For each recording (Rec 01 -> Rec 10), the calibration data is plotted.

#%%
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 170

for rec, rec_df in dict_of_recordings.items():
    only_calibration = rec_df.loc[rec_df['ElementType'] == 'CalibrationPoint']
    ax = only_calibration.plot.scatter(
        'FixationPointX',
        'FixationPointY',
        c='GazeEventDuration',
        colormap='viridis')
    ax.plot(1366 / 2, 768 / 2, 'r+', markersize=14)
    ax.set_xlim(0, 1366)
    ax.set_ylim(0, 768)
    ax.set_title(rec)

#%% [markdown]
# ## Systematic and random error
# Calculate systematic error by taking the average position of
# fixations on the calibration image for each recording

#%%
from aptipy.analysis.utilities import wavg, wvar

for rec, rec_df in dict_of_recordings.items():
    only_calibration = rec_df.loc[rec_df['ElementType'] == 'CalibrationPoint']
    wmean_x = wavg(only_calibration, 'FixationPointX', 'GazeEventDuration')
    wmean_y = wavg(only_calibration, 'FixationPointY', 'GazeEventDuration')

    wvar_x = wvar(only_calibration, 'FixationPointX', 'GazeEventDuration')
    wvar_y = wvar(only_calibration, 'FixationPointY', 'GazeEventDuration')

    plt.figure()
    plt.errorbar(
        wmean_x, wmean_y, xerr=np.sqrt(wvar_x), yerr=np.sqrt(wvar_y), fmt='x')
    plt.plot(1366 / 2, 768 / 2, 'r+', markersize=14)
    plt.xlim(0, 1366)
    plt.ylim(0, 768)
    plt.title(rec)

#%% [markdown]
# ## Plotting on an image (TEST)

#%%
img_parent_path = r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S8\MPhys_s8\test_images_2'
boyceimg = plt.imread(img_parent_path + r'\boyce.jpg')

rec10_df = dict_of_recordings['Rec 10']
isboyce = rec10_df['MediaName'] == 'boyce.jpg'
isdata = rec10_df['ElementType'] == 'DataPoint'

boyce_df = rec10_df.loc[isboyce & isdata]

boyce_df.plot.scatter(
    'FixationPointX',
    'FixationPointY',
    c='GazeEventDuration',
    colormap='viridis')
plt.imshow(boyceimg, extent=[0, 1024, 0, 598])
#%%
