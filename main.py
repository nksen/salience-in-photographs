"""
--Naim Sen--
--Toby Ticehurst--

main.py

"""

## ==== Imports ==== ##
import cv2
import preprocessing
import directions_factory
import numpy as np
import bounding_box
import argparse
from pathlib import Path

# declare parser
parser = argparse.ArgumentParser()
parser.add_argument("img_path", help="path to image file", type=str)
args = parser.parse_args()
org_img_path = Path(args.img_path)
if not org_img_path.is_file():
    raise ValueError("Invalid image file path. File does not exist.")
# load image
org_img = cv2.imread(str(org_img_path.resolve()))
if org_img is not None:
    pass
else:
    raise ValueError("Invalid image file path.")

print(org_img.shape)
# process image
s_map = preprocessing.generate_saliency_map(org_img, to_display=True)
# generate box and directions
y = s_map.shape[0]
x = s_map.shape[1]
starting_box = bounding_box.Box(s_map, np.array([0, 0]), np.array([int(y/3), int(x/3)]), np.array([int(y/50), int(x/50)]))
directions_list = directions_factory.unconstrained()
# minimise salience
lowest_cost_box = bounding_box.minimise_cost(starting_box, 50, 70, directions_list)
lowest_cost_box.playback_history(
    #s_map,
    cv2.imread(str(org_img_path.resolve()), 0),
    '../mphys-testing/salience-in-photographs/images/output')
cv2.waitKey(0)
