"""
--Naim Sen--
--Toby Ticehurst--

box_factory.py

for creating template starting boxes (in bulk) by translating
readable, image-agnostic requests into image-specific co-ordinates
that are passed to the box constructor. Acts as an interface layer
between the Box mechanics and the user-facing GUI/CLI.
"""

# std imports
import cv2
import numpy as np
# module imports
import bounding_box

class BoxFactory(object):
    """
    BoxFactory encapsulates all template generation of the
    box. Should be able to create multiple boxes .
    """

    def __init__(self, s_map, text=None):
        self._s_map = s_map
        # initialise requests list
        self._requests_list = None
        if text is None:
            self._min_size = np.array([0, 0])
#        else:
#            self._min_size = text.smallest_width()

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
            box_dims = box_dims * img_shape
            box_dims = box_dims.astype(int)
        else:
            raise AssertionError("Invalid request: dimensions must be either float or ndarray")

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
            i = int(img_shape[0]/2) - int(box_dims[0]/2)
            j = int(img_shape[1]/2) - int(box_dims[1]/2)
        elif pos_readable == "cl":
            i = int(img_shape[0]/2) - int(box_dims[0]/2)
            j = 0
        elif pos_readable == "cr":
            i = int(img_shape[0]/2) - int(box_dims[0]/2)
            j = img_shape[1] - box_dims[1]
        elif pos_readable == "ct":
            i = 0
            j = int(img_shape[1]/2) - int(box_dims[1]/2)
        elif pos_readable == "cb":
            i = img_shape[0] - box_dims[0]
            j = int(img_shape[1]/2) - int(box_dims[1]/2)
        else:
            if isinstance(pos_readable, str):
                raise ValueError("Invalid request.")
            else:
                raise AssertionError("Invalid request: position must be str instance.")
        # construct position array
        pos = np.array([i,j])

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
        for request in self._requests_list:
            box_tl = request[0]
            box_dims = request[1]
            box = bounding_box.Box(self._s_map, box_tl, box_dims, self._min_size)
            boxes_list.append(box)
        return boxes_list
        

if __name__ == "__main__":
    image = cv2.imread("../mphys-testing/images/footballer.jpg", 0)
    requests = [["br", 0.2],
                ["tl", 0.5]
                ]
    factory = BoxFactory(image)
    boxes = factory.generate_boxes(requests)
    outimg = boxes[1].overlay_box(image)
    cv2.imshow("outimg", outimg)
    cv2.waitKey(0)