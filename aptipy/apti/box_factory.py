"""
--Naim Sen--
--Toby Ticehurst--

Dec 2018

box_factory.py

for creating template starting boxes (in bulk) by translating
readable, image-agnostic requests into image-specific co-ordinates
that are passed to the box constructor. Acts as an interface layer
between the Box mechanics and the user-facing GUI/CLI.

Copyright © 2018, Naim Sen
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>
"""

# std imports
import os
from multiprocessing import Pool
from multiprocessing import cpu_count
from pathlib import Path
import numpy as np
import cv2
# module imports
from ..apti import bounding_box


class BoxFactory(object):
    """
    BoxFactory encapsulates all template generation of the
    box. Should be able to create multiple boxes .
    """

    def __init__(self, s_map, headline=None):
        self._s_map = s_map
        # initialise requests list
        self._requests_list = None

        if headline is not None:
            self._text_ctx = headline
            self._min_size, self._min_area = headline.get_constraints()
        else:
            self._text_ctx = None
            self._min_size = np.array([0, 0])
            self._min_area = 0

    # ~~ Properties ~~ #
    @property
    def positions_list(self):
        return [
            #"top left",
            "tl",
            #"top right",
            "tr",
            #"bottom left",
            "bl",
            #"bottom right",
            "br",
            #"centered",
            "c",
            #"centre left",
            "cl",
            #"centre right",
            "cr",
            #"centre top",
            "ct",
            #"centre bottom",
            "cb"
        ]

    def translate_request(self, request_readable):
        """
        Translates a single request
        """
        # unpack request
        pos_readable = request_readable[0]
        box_dims = request_readable[1]
        # get image shape
        img_shape = np.array(self._s_map.shape)

        # construct dims array
        if isinstance(box_dims, np.ndarray):
            pass
        elif isinstance(box_dims, float) and box_dims < 1 and box_dims > 0:
            # for passing box_dims as a fraction of image size
            box_dims = np.sqrt(box_dims) * img_shape
            box_dims = box_dims.astype(int)
        else:
            raise AssertionError(
                "Invalid box_factory request: dimensions must be either float or ndarray"
            )

        # account for all template locations
        if pos_readable == "tl":
            i = 0
            j = 0
        elif pos_readable == "tr":
            i = 0
            j = img_shape[1] - box_dims[1]
        elif pos_readable == "bl":
            i = img_shape[0] - box_dims[0]
            j = 0
        elif pos_readable == "br":
            i = img_shape[0] - box_dims[0]
            j = img_shape[1] - box_dims[1]
        elif pos_readable == "c":
            i = int(img_shape[0] / 2) - int(box_dims[0] / 2)
            j = int(img_shape[1] / 2) - int(box_dims[1] / 2)
        elif pos_readable == "cl":
            i = int(img_shape[0] / 2) - int(box_dims[0] / 2)
            j = 0
        elif pos_readable == "cr":
            i = int(img_shape[0] / 2) - int(box_dims[0] / 2)
            j = img_shape[1] - box_dims[1]
        elif pos_readable == "ct":
            i = 0
            j = int(img_shape[1] / 2) - int(box_dims[1] / 2)
        elif pos_readable == "cb":
            i = img_shape[0] - box_dims[0]
            j = int(img_shape[1] / 2) - int(box_dims[1] / 2)
        else:
            if isinstance(pos_readable, str):
                raise ValueError("Invalid request.")
            else:
                raise AssertionError(
                    "Invalid request: position must be str instance.")
        # construct position array
        pos = np.array([i, j])

        return [pos, box_dims]

    def load_requests(self, requests_readable):
        """
        Allows us to load requests into the factory before generating boxes. 
        Called internally by generate_boxes.
        """
        self._requests_list = []
        # convert requests
        for request in requests_readable:
            self._requests_list.append(self.translate_request(request))
        # check lengths match
        if len(self._requests_list) == len(requests_readable):
            return True
        else:
            return False

    def generate_boxes(self, requests_readable=None):
        """
        Generates boxes according to requests. If requests are given during function call,
        the internal requests list is overwritten.
        """
        if requests_readable is None and self._requests_list is None:
            raise AttributeError("generate_boxes(): requests_list is NoneType")
        elif requests_readable is not None:
            self.load_requests(requests_readable)
        boxes_list = []

        # loop over requests and generate boxes
        for index, request in enumerate(self._requests_list):
            box_tl = request[0]
            box_dims = request[1]
            box = bounding_box.Box(self._s_map, box_tl, box_dims,
                                   self._min_size, self._min_area)
            # add request metadata
            box.metadata.construction_request = requests_readable[index]
            box.metadata.headline_raw = str(self._text_ctx)
            boxes_list.append(box)
        return boxes_list


def minimise_boxes(boxes_list,
                   directions_lists,
                   step_size=10,
                   n_iterations=10000):
    """
    Utilises multiprocessing.Pool to minimise multiple boxes simultaneously. 
    num workers is cpu_count - 1 to prevent complete CPU lockup.
    """
    # check if step size is a list or int
    # if int, make into list of ints so it can be passed to starmap
    if isinstance(step_size, int):
        step_size = [step_size] * len(boxes_list)
    elif not isinstance(step_size, list):
        raise ValueError(
            "minimise_boxes: step size should be int or list with length == len(boxes_list)"
        )

    # same check with n_iterations
    if isinstance(n_iterations, int):
        n_iterations = [n_iterations] * len(boxes_list)
    elif not isinstance(n_iterations, list):
        raise ValueError(
            "minimise_boxes: n iterations should be int or list with length == len(boxes_list)"
        )

    # make ndarray of list sizes and check that they're the same
    lengths = np.array([
        len(boxes_list),
        len(directions_lists),
        len(step_size),
        len(n_iterations)
    ])

    if not np.all(lengths == lengths[0]):
        print(lengths)
        raise ValueError(
            "minimise_boxes: argument arrays must have equal lengths.")

    # repack boxes_list directions_lists step_size and n_iterations into an iterable
    # such that: [(1,2), (3,4)] -> [func(1,2), func(3,4)]
    args_iterable = zip(boxes_list, directions_lists, step_size, n_iterations)
    """
    args_iterable = []
    for index in range(len(boxes_list)):
        arguments = (boxes_list[index], directions_lists[index], step_size[index], n_iterations[index])
        args_iterable.append(arguments)
    """
    # get process number and open pool
    num_workers = cpu_count() - 1
    print("Opening pool")
    with Pool(processes=num_workers) as pool:
        optimum_boxes = pool.starmap(bounding_box.minimise_cost, args_iterable)
        pool.close()
        print("Pool closed")
        pool.join()

    return optimum_boxes


def write_boxes(boxes_list, folderpath, imagepath, headline=None):
    """
    Saves a list of boxes to the folder specified by folderpath.
    Directory structure is created:
        $Image name$
            $requestanchor$
                --files stored here--
    
    headline kwarg passess through to box.write_to_file
    """
    # create top level directory
    parent_path = folderpath / Path(imagepath.stem)
    if parent_path.is_dir():
        raise ValueError("write_boxes: directory ", str(parent_path),
                         " exists")
    parent_path.resolve().mkdir()

    # loop over boxes
    for box in boxes_list:
        # create box path
        if box.metadata.construction_request is None:
            box_path = parent_path / Path(str(box.metadata.box_id))
        else:
            box_path = parent_path / Path(box.metadata.construction_request[0])
        # make box directory
        if box_path.is_dir():
            raise ValueError("write_boxes: directory ", str(box_path),
                             " exists")
        box_path.mkdir()
        # write box data to file
        box.write_to_file(box_path, imagepath, headline=headline)


if __name__ == "__main__":
    image = cv2.imread("../mphys-testing/images/footballer.jpg", 0)
    requests = [["br", 0.2], ["tl", 0.5]]
    factory = BoxFactory(image)
    boxes = factory.generate_boxes(requests)
    outimg = boxes[1].overlay_box(image)
    cv2.imshow("outimg", outimg)
    cv2.waitKey(0)
