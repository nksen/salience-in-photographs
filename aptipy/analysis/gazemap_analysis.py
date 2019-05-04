"""
--Naim Sen--

Apr 19

Comparison of gazemap (ground-truth) with apti results

Copyright © 2019, Naim Sen
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>
"""

#%% [markdown]
# # Gaze maps and apti
# Now we can test the results of the apti procedure by comparison
# with the gaze maps we produced earlier.
#
#
# First, we need to load the gaze maps and the apti results.
# We also need to import all our apti modules

#%%
%matplotlib inline
import os
import pickle
from pathlib import Path
import pandas as pd

import cv2
import matplotlib.pyplot as plt

import aptipy.analysis.utilities as utilities
from aptipy.apti import bounding_box, box_factory

#%%
# First get gazemaps (the easier bit)

folderpath = r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S8\MPhys_s8\eyetracking_analysis\gazemaps'
gazemaps_dict = dict()
for file in os.listdir(folderpath):
    img_name = utilities.remove_prefix(file, 'gazemap_')
    filepath = folderpath + '\\' + file
    gazemaps_dict[img_name] = cv2.imread(filepath, 0)

#%%
# Now we need to get all 180 different headline positions

toplevel_path = Path(
    r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S8\MPhys_s8\results\first_run'
)
boxes_dict = dict()
for img_name in gazemaps_dict:
    img_name_noext = Path(img_name).stem
    # remove ext
    midlevel_path = toplevel_path / Path(img_name).stem
    # Just in case something gets garbled between image names and folder names
    if midlevel_path.is_dir():
        pass
    else:
        raise OSError(str(midlevel_path), 'Does not exist.')

    # loop over the 9 box positions
    results_subdict = dict()
    pos_list = box_factory.positions_list()
    for pos in pos_list:
        # get baselevel path and construct filename
        baselevel_path = midlevel_path / pos
        metafile_name = 'metadata_' + pos + '_' + img_name_noext + '.pkl'

        with (baselevel_path / metafile_name).open('rb') as file:
            metafile = pickle.load(file)
        results_subdict[pos] = metafile

    boxes_dict[img_name] = results_subdict

#%% [markdown]
# ##
# With all the bits loaded, we now want to construct a gazebox and measure the
# gaze density for each box position. Any invalid text positions will be discarded.
# We store the results as a pandas dataframe.
#%%
results_df = pd.DataFrame(columns=['MediaName', 'BoxPosition', 'BoxGazeDensity', 'TotalGazeDensity'])
for img_name, gazemap in gazemaps_dict.items():
    for box_pos, metadata in boxes_dict[img_name].items():
        # temporary dictionary to store a row
        row_dict = {'MediaName': img_name, 'BoxPosition': box_pos}
        
        # get tl and dims to construct gaze box
        box_tl = [metadata.headline_tl[1], metadata.headline_tl[0]]
        box_dims = [
            metadata.headline_br[1] - metadata.headline_tl[1],
            metadata.headline_br[0] - metadata.headline_tl[0]
        ]

        # construct GazeBox
        try:
            from aptipy.apti.preprocessing import generate_saliency_map

            # load image and generate smap
            raw_img = cv2.imread(r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S8\MPhys_s8\test_images_2' + '\\' + img_name)

            smap = generate_saliency_map(raw_img)
            gazebox = utilities.GazeBox(gazemap, box_tl, box_dims)
            sbox = bounding_box.Box(smap, box_tl, box_dims)
            gazemap_with_overlay = gazebox.overlay_box(gazemap)

            # append to row dict
            row_dict['OrgBoxCost'] = metadata.cost_history[-1]
            row_dict['HeadlineCost'] = sbox.cost
            row_dict['BoxGazeDensity'] = gazebox.gaze_heat_density
            row_dict['TotalGazeDensity'] = gazebox.total_heat_density

        except:
            # append NaN to row if results are invalid
            row_dict['BoxGazeDensity'] = None
            row_dict['TotalGazeDensity'] = None
        results_df = results_df.append(row_dict, ignore_index=True)

results_df['FractionalGazeDensity'] = results_df['BoxGazeDensity'] / results_df['TotalGazeDensity']
with pd.option_context('display.max_rows',None):
    display(results_df)

#%% [markdown]
# ## Export and visualisation
# Now export the dataframe for safekeeping.


#%%
savepath = r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S8\MPhys_s8\eyetracking_analysis\gazedata_results.xlsx'
results_df.to_excel(savepath)


#%% [markdown]
# ## Boxes with lowest fractional gaze density
#%%
gaze_based_selection = results_df.loc[results_df.groupby(['MediaName'])['FractionalGazeDensity'].idxmin()]
hlcost_based_selection = results_df.loc[results_df.groupby(['MediaName'])['HeadlineCost'].idxmin()]
boxcost_based_selection = results_df.loc[results_df.groupby(['MediaName'])['OrgBoxCost'].idxmin()]

selection_overlap = pd.merge(gaze_based_selection, hlcost_based_selection, how='inner', on=['BoxGazeDensity'])
boxselection_overlap = pd.merge(gaze_based_selection, boxcost_based_selection, how='inner', on=['BoxGazeDensity'])

with pd.option_context('display.max_rows',None):
    display("gaze based selection", gaze_based_selection)
    display("box-cost based selection", boxcost_based_selection)
    display("headline-cost based selection", hlcost_based_selection)
    display("headline/gaze overlap", selection_overlap)
    display("box/gaze overlap", boxselection_overlap)
#%%
