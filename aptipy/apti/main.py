"""
--Naim Sen--

main.py

Copyright © 2018, Naim Sen
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>
"""

## ==== Imports ==== ##
# std imports
import cv2
import numpy as np
import argparse
from pathlib import Path
# module imports
from ..apti import preprocessing, bounding_box, box_factory
from ..apti import directions_factory as df
from ..scrape_headlines.requester import Requester
from ..apti.text import Text


def main(img_path, savefolder):
    """
    main function for running the minimisation on a test image
    """
    ## save path ##
    # check if optional savepath has been given
    # if not specified, the root directory is used
    if savefolder is not None:
        parent_save_path = Path.home() / Path(savefolder)
        print(parent_save_path)
    else:
        parent_save_path = Path.cwd()

    ## image path ##
    raw_img_path = Path.home() / Path(img_path)
    # check that image exists
    if not raw_img_path.is_file():
        raise ValueError("Invalid image file path. File does not exist.")

    # ==== load & process image ==== #
    raw_img = cv2.imread(str(raw_img_path.resolve()))
    if raw_img is not None:
        pass
    else:
        raise ValueError("Invalid image file path.")
    # process image
    s_map = preprocessing.generate_saliency_map(raw_img, to_display=True)

    # ==== get a headline and measure ==== #
    headline_server = Requester()
    headline_raw, headline_idx = headline_server.get()
    print("HL ", headline_idx, ": ", headline_raw)

    fontpath = Path(
        r'../salience-in-photographs/aptipy/assets/BBCReith/BBCReithSans_Bd.ttf'
    )
    text_ctx = Text(headline_raw, fontpath.resolve())
    text_ctx.rescale_font_size(s_map.shape)

    # ==== generate boxes and directions ==== #
    factory = box_factory.BoxFactory(s_map, headline=text_ctx)
    #factory = box_factory.BoxFactory(s_map)
    # generate requests for the factory
    box_init_size = 0.3  # this can be expressed as an ndarray or as a fraction of image size
    requests = [["tl", box_init_size], ["tr", box_init_size],
                ["bl", box_init_size], ["br", box_init_size],
                ["c", box_init_size], ["cl", box_init_size],
                ["cr", box_init_size], ["ct", box_init_size],
                ["cb", box_init_size]]
    box_list = factory.generate_boxes(requests_readable=requests)
    """
    # TESTING
    for box in box_list:
        title = box.metadata.construction_request[0]
        cv2.imshow(title, box.overlay_box(raw_img))
        cv2.waitKey(0)
    """
    # declare directions list list

    directions = [
        df.topleft_anchored(),
        df.topright_anchored(),
        df.bottomleft_anchored(),
        df.bottomright_anchored(),
        df.unconstrained(),
        df.left_anchored(),
        df.right_anchored(),
        df.top_anchored(),
        df.bottom_anchored()
    ]

    box_list = box_factory.minimise_boxes(box_list, directions)
    """
    for box in box_list:
        img = box.overlay_box(raw_img)
        cv2.imshow(box.metadata.construction_request[0], img)
        cv2.waitKey(0)
    """

    # write boxes
    box_factory.write_boxes(
        box_list, parent_save_path, raw_img_path, headline=text_ctx)
    """
   
    # minimise salience
    lowest_cost_box = bounding_box.minimise_cost(starting_box, 50, 70, directions_list)
    lowest_cost_box.playback_history(
        #s_map,
        cv2.imread(str(org_img_path.resolve()), 0),
        '../mphys-testing/salience-in-photographs/images/output')
    cv2.waitKey(0)
    """


def run_on_file():
    # ==== handle user input ==== #
    # declare parser
    parser = argparse.ArgumentParser()
    # add args
    parser.add_argument("img_path", help="path to image file", type=str)
    parser.add_argument(
        "-f", help="path to output",
        type=str)  # this argument is optional (defaults to NoneType)

    # grab args
    args = parser.parse_args()

    # run main
    main(args.img_path, args.f)


def run_on_folder():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="path to image directory", type=str)
    parser.add_argument(
        "-f", help="path to output directory", type=str)  # optional

    args = parser.parse_args()
    # get files in dir
    img_dir = Path.home() / Path(args.dir)
    for img in img_dir.iterdir():
        main(img, args.f)


if __name__ == "__main__":
    run_on_folder()
