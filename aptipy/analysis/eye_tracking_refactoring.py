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
display(results_df.head(10))
#%% [markdown]
# # clean the data of useless columns etc.
#%%
# print out columns
display(results_df.columns.values)
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
display(results_df.head(10))
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

display(results_df)

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
plt.rcParams['figure.dpi'] = 150

for rec, rec_df in dict_of_recordings.items():
    only_calibration = rec_df.loc[rec_df['ElementType'] == 'CalibrationPoint']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.scatter(
        only_calibration['FixationPointX'],
        only_calibration['FixationPointY'],
        marker='x',
        c=only_calibration['GazeEventDuration'],
        cmap='viridis')
    ax.plot(1366 / 2, 768 / 2, 'r+', markersize=14)
    ax.set_xlim(0, 1366)
    ax.set_ylim(0, 768)
    ax.set_xlabel('Fixation point X /px')
    ax.set_ylabel('Fixation point Y /px')
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Gaze event duration /ms')
    ax.set_title(rec)

#%% [markdown]
# ## Systematic and random error
# Calculate systematic error by taking the average position of
# fixations on the calibration image for each recording

#%%
from aptipy.analysis.utilities import wavg, wvar, wcov

errors_dict = dict()
variances = []
for rec, rec_df in dict_of_recordings.items():
    only_calibration = rec_df.loc[rec_df['ElementType'] == 'CalibrationPoint']
    wmean_x = wavg(only_calibration, 'FixationPointX', 'GazeEventDuration')
    wmean_y = wavg(only_calibration, 'FixationPointY', 'GazeEventDuration')

    wvar_x = wvar(only_calibration, 'FixationPointX', 'GazeEventDuration')
    wvar_y = wvar(only_calibration, 'FixationPointY', 'GazeEventDuration')
    wcov_xy = wcov(only_calibration, 'FixationPointX', 'FixationPointY',
                   'GazeEventDuration')

    errors_dict[rec] = [(wmean_x, wmean_y), (wvar_x, wvar_y, wcov_xy)]
    current_vars = [np.sqrt(wvar_x), np.sqrt(wvar_y)]
    variances.append(current_vars)
    # plt.figure()
    # plt.errorbar(
    #     wmean_x, wmean_y, xerr=np.sqrt(wvar_x), yerr=np.sqrt(wvar_y), fmt='x')
    # plt.plot(1366 / 2, 768 / 2, 'r+', markersize=14)
    # plt.xlim(0, 1366)
    # plt.ylim(0, 768)
    # plt.xlabel('Mean fixation point X')
    # plt.ylabel('Mean fixation point Y')
    # plt.title(rec)

#%%
variances = np.array(variances)
meanvar = np.mean(variances,axis=0)
#meanvar = np.mean([errors_dict.values()[]])
#%% [markdown]
# ## Testing systematic correction:
# The systematic offset is calculated for each recording and subtracted
# from each datapoint. A pair of example plots are shown below.

#%%
from PIL import Image

img_parent_path = r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S8\MPhys_s8\test_images_2'
#boyceimg = plt.imread(img_parent_path + r'\boyce.jpg', )
boyceimg = Image.open(img_parent_path + r'\boyce.jpg', 'r').convert('LA')

temp_rec_df = dict_of_recordings['Rec 01']
isboyce = temp_rec_df['MediaName'] == 'boyce.jpg'
isdata = temp_rec_df['ElementType'] == 'DataPoint'

boyce_df = temp_rec_df.loc[isboyce & isdata]

plt.scatter(
    boyce_df['FixationPointX'],
    boyce_df['FixationPointY'],
    c=boyce_df['GazeEventDuration'],
    cmap='viridis')
plt.imshow(boyceimg, extent=[0, 1024, 0, 598])
cbar = plt.colorbar()
cbar.set_label('Gaze event duration /ms')
plt.xlabel('Unadjusted fixation point X /px')
plt.ylabel('Unadjusted fixation point Y /px')
plt.title('boyce.jpg Rec 01 without correction')
#%%
# Now subtract the systematic away
x_offset = errors_dict['Rec 01'][0][0] - 1366 / 2
y_offset = errors_dict['Rec 01'][0][1] - 768 / 2

boyce_df.loc[:,
             'FixationPointY'] = boyce_df.loc[:, 'FixationPointY'] - y_offset
boyce_df.loc[:,
             'FixationPointX'] = boyce_df.loc[:, 'FixationPointX'] - x_offset

plt.figure()
plt.scatter(
    boyce_df['FixationPointX'],
    boyce_df['FixationPointY'],
    c=boyce_df['GazeEventDuration'],
    cmap='viridis')
plt.imshow(boyceimg, extent=[0, 1024, 0, 598])
cbar = plt.colorbar()
cbar.set_label('Gaze event duration /ms')
plt.xlabel('Adjusted fixation point X /px')
plt.ylabel('Adjusted fixation point Y /px')
plt.title('boyce.jpg Rec 01 with correction')

#%% [markdown]

# As shown above, the systematic offset estimation seems to work.
# The fixations now align with our expectations of where participants
# are looking.
#
# ## Now correct the entire dataset...
# Also add columns for error and a column for the GazeEventDuration as a fraction
# of the time that the image is shown for - (5000 ms)
#%%
# Copy dataframe (only datapoints)
adjusted_df = results_df[results_df.ElementType == 'DataPoint']
display(adjusted_df)

for rec, val in errors_dict.items():
    x_offset = val[0][0] - 1366 / 2
    y_offset = val[0][1] - 768 / 2

    is_rec = adjusted_df['RecordingName'] == rec
    adjusted_df.loc[is_rec, 'FixationPointX'] -= x_offset
    adjusted_df.loc[is_rec, 'FixationPointY'] -= y_offset

    adjusted_df.loc[is_rec, 'FixationPointXErr'] = np.sqrt(val[1][0])
    adjusted_df.loc[is_rec, 'FixationPointYErr'] = np.sqrt(val[1][1])
    adjusted_df.loc[is_rec, 'FixationPointXYCov'] = val[1][2]

adjusted_df.loc[:,
                'GazeEventProportion'] = adjusted_df.loc[:,
                                                         'GazeEventDuration'] / 5000
display(adjusted_df)
#%%
import matplotlib.cm
from matplotlib.colors import Normalize

plt.figure()
xvals = adjusted_df.loc[adjusted_df.MediaName == 'boyce.jpg', 'FixationPointX']
yvals = adjusted_df.loc[adjusted_df.MediaName == 'boyce.jpg', 'FixationPointY']
xerr = adjusted_df.loc[adjusted_df.MediaName ==
                       'boyce.jpg', 'FixationPointXErr']
yerr = adjusted_df.loc[adjusted_df.MediaName ==
                       'boyce.jpg', 'FixationPointYErr']
duration = adjusted_df.loc[adjusted_df.MediaName ==
                           'boyce.jpg', 'GazeEventProportion'].values

# Convert duration to colour map
cmap = matplotlib.cm.Reds
norm = Normalize(vmin=duration.min(), vmax=duration.max())

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

plt.errorbar(
    xvals,
    yvals,
    xerr=xerr,
    yerr=yerr,
    fmt='none',
    elinewidth=1,
    ecolor=cmap(norm(duration)))
cbar = plt.colorbar(
    mappable=sm, ticks=np.linspace(min(duration), max(duration), num=5))
cbar.set_label('Fractional gaze event duration')
plt.imshow(boyceimg, extent=[0, 1024, 0, 598])
#plt.colorbar(cmap=cmap, norm=norm(duration))
#cbar.set_label('Gaze event duration /ms')
plt.xlabel('Adjusted fixation point X /px')
plt.ylabel('Adjusted fixation point Y /px')
plt.title('boyce.jpg all recordings (adjusted)')

#%%
from aptipy.analysis.utilities import load_images
image_dict = load_images(img_parent_path)

for medianame, image in image_dict.items():
    xvals = adjusted_df.loc[adjusted_df.MediaName ==
                            medianame, 'FixationPointX']
    yvals = adjusted_df.loc[adjusted_df.MediaName ==
                            medianame, 'FixationPointY']
    xerr = adjusted_df.loc[adjusted_df.MediaName ==
                           medianame, 'FixationPointXErr']
    yerr = adjusted_df.loc[adjusted_df.MediaName ==
                           medianame, 'FixationPointYErr']
    duration = adjusted_df.loc[adjusted_df.MediaName ==
                               medianame, 'GazeEventProportion'].values

    plt.figure()

    # Convert duration to colour map
    cmap = matplotlib.cm.Reds
    norm = Normalize(vmin=duration.min(), vmax=duration.max())

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    plt.errorbar(
        xvals,
        yvals,
        xerr=xerr,
        yerr=yerr,
        fmt='none',
        elinewidth=1,
        ecolor=cmap(norm(duration)))
    cbar = plt.colorbar(
        mappable=sm, ticks=np.linspace(min(duration), max(duration), num=5))
    cbar.set_label('Fractional gaze event duration')
    plt.imshow(image, extent=[0, image.shape[1], 0, image.shape[0]])
    plt.xlabel('Adjusted fixation point X /px')
    plt.ylabel('Adjusted fixation point Y /px')
    plt.title(medianame + ' adjusted')
#%% [markdown]
# ## Export all the things

# #%%
# import pickle

# adjusted_df.to_excel(
#     r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S8\MPhys_s8\eyetracking_analysis\adjusted_gazedata.xlsx'
# )

# pickle.dump(image_dict, (open(
#     r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S8\MPhys_s8\eyetracking_analysis\images_dict.pkl',
#     'wb')))

# #%%
