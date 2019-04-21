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
# With all the bits loaded, we now want to construct a gazebox and measure all the 

#%%
for img_name, gazemap in gazemaps_dict.items():
    for box_pos, metadata in boxes_dict[img_name].items():
        # get tl and dims to construct box
        #display(metadata.__dict__)
        box_tl = [metadata.headline_tl[1], metadata.headline_tl[0]]
        box_dims = [
            metadata.headline_br[1] - metadata.headline_tl[1],
            metadata.headline_br[0] - metadata.headline_tl[0]
        ]

        # construct GazeBox
        try:
            gazebox = utilities.GazeBox(gazemap, box_tl, box_dims)
            gazemap_with_overlay = gazebox.overlay_box(gazemap)
        except:
            display("BROKE HERE")
            display(gazemap.shape)
            display(metadata.__dict__)
            display(img_name)
        #fig = plt.figure()
        #ax = fig.add_subplot(111)
        #ax.imshow(gazemap_with_overlay)
        title_str = img_name + ' ' + box_pos
        #ax.set_title(title_str)

        display(title_str)
        display("box cost: %f" % (gazebox.cost))
        display("image cost: %f" % gazebox.total_cost)
        #display(fig)
        display('---------------------------------------------------')
        #plt.close() # needed to suppress ipy auto output
    
#%%
meta = boxes_dict['eoin_morgan_getty.jpg']['tr']
display(meta.__dict__)
gazemaps_dict['eoin_morgan_getty.jpg'].shape
#%%
