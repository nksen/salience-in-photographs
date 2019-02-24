"""
--Naim Sen--
--Toby Ticehurst--

Oct 2018

bounding_box.py

Box class and accompanying functions.

Copyright © 2018, Naim Sen 
Licensed under the terms of the GNU General Public License
<https://www.gnu.org/licenses/gpl-3.0.en.html>
"""

# std imports
import os
import cv2
import PIL
import copy
import binascii
import numpy as np
from pathlib import Path
# module imports
import utilities


class Box(object):
    """
    The box is a submatrix of the image, with an anchor point
    defined as the upper left corner, and dimensions. Indices
    follow the matrix (i,j) convention.

    #Properties

        shape  : Dimensions of the box in (i,j)
        box_tl : Co-ords for the top left corner of the box,
                 used as the anchor point.
        box_br : Co-ords for the bottom right corner of the box,
                 computed from box_tl & shape.
        image  : np.array grayscale saliency map which the box is
                 to be drawn over.
        data   : Segment of the image matrix that is covered by the
                 box. This is updated if the box is translated or
                 resized.    
    """
    def __init__(self, s_map, box_tl, dims, minimum_size=np.array([0, 0])):
        """
        Box object initialiser
        Args:
            s_map: np.array grayscale saliency map which the box is
                          to be drawn over.
            box_tl: Co-ords for the bottom right corner of the box,
                    computed from box_tl & dims
            dims: Dimensions of the box in (i,j). Presented as shape
                  property later to avoid confusion.

        Raises:
            ValueError: For any invalid dimension. This raise should
                        also be used for any further constraints on
                        the size/shape/position.
        """
        # check that box_tl and dims are non-negative
        if any(element < 0 for element in box_tl):
            raise ValueError("Anchor point must be non-negative.")
        if any(element < 0 for element in dims):
            raise ValueError("Dimensions must be non-negative.")
        if any(element < 0 for element in minimum_size):
            raise ValueError("Min size must be non-negative.")
        
        # check that dimensions are large than minimum_size
        if dims[0] < minimum_size[0]:
            raise ValueError("i'th dimension is less than minimum size.")
        if dims[1] < minimum_size[1]:
            raise ValueError("j'th dimension is less than minimum size.")
        
        # assign vars
        self._box_tl = box_tl
        self._dims = dims
        self._s_map = s_map
        self._min_size = minimum_size
        # compute and check box_br
        box_br = np.add(box_tl, dims)
        if box_br[0] > s_map.shape[0] or box_br[1] > s_map.shape[1]:
            raise ValueError("Box drawn out of range.\n" + str(box_br))
        else:
            self._box_br = box_br
        
        # grab data inside box from s_map
        # create numpy mask
        mask_i = np.arange(box_tl[0], box_br[0], 1).tolist()
        mask_j = np.arange(box_tl[1], box_br[1], 1).tolist()
        ixgrid = np.ix_(mask_i, mask_j)
        # assign data
        self._data = s_map[ixgrid]

        # declare metadata Bunch type and initialise values
        self._metadata = utilities.Bunch(
            box_id=binascii.b2a_hex(os.urandom(15)),
            history=[],
            cost_history=[],
            construction_request=None,       # used to store raw request made by factory if box was created in a factory
            starting_box_tl=box_tl,
            starting_dims=dims,
            n_transformations=0
        )

    # ~~ Properties ~~ #
    @property
    def box_tl(self):
        return self._box_tl

    @property
    def box_br(self):
        return self._box_br
  
    @property
    def shape(self):
        return self._dims

    @property
    def data(self):
        return self._data

    @property
    def s_map(self):
        return self._s_map

    @property
    def cost(self):
        """
        Calculates the cost bounded by the box.
        Changing to a more detailed calculation.
        """
        return np.sum(self._data)/(self.shape[0] * self.shape[1]) ** 2

    @property
    def metadata(self):
        """
        Returns metadata Bunch
        Bunch has the following items:
    
        """
        return self._metadata

    # ~~ Methods ~~ #
    def transform(self, vector, record_transformation=False):
        """
        Transforms the box according to the specified vector by
        calling the translate and resize methods

        Args:
            vector: Compound vector of shape 2x2. The first element is the
                    translation vector, and the second is the resize
                    vector.
            record_transformation: Bool to allow addition of provided vector to
                                   the metadata.history
        Returns:
            N/A: modifies self by calling resize and translate (consider returning
                 success flag if necessary?
        Raises:
        """
        # cache metadata
        metadata = self._metadata
        # translate box
        new_anchor = np.add(self._box_tl, vector[0])
        self.__init__(self.s_map, new_anchor, self.shape, self._min_size)
        # resize box
        new_dims = np.add(self._dims, vector[1])
        self.__init__(self.s_map, self.box_tl, new_dims, self._min_size)
        # reassign metadata
        self._metadata = metadata
        # update metadata history if required
        if record_transformation:
            self._metadata.history.append(vector)

    def overlay_box(self, image):
        """
        Overlays a blue box on the image provided (note, not on own
        image).
        Args:
            image: np.array or PIL.Image.Image of the image that the
            box is to be drawn on.
        Returns:
            img_with_overlay: The image with the overlaid box.
        Raises:
       
        """

        # define tuples for cv2.rectangle
        colour = (255, 0, 0)
        # cv2.rectangle requires corner co-ordinates to be in (x,y) not (i,j)
        # so indices are flipped.
        tl_tuple = tuple(np.flip(self.box_tl, 0))
        br_tuple = tuple(np.flip(self.box_br, 0))

        # Handle CV images
        if isinstance(image, np.ndarray):
            # copy image
            img_with_overlay = copy.copy(image)
            # check if image is colour or greyscale
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            # get stroke width from image dimensions
            stroke_width = utilities.estimate_stroke_width(img_with_overlay.shape)
            # draw rectangle
            cv2.rectangle(img_with_overlay, tl_tuple, br_tuple, colour, stroke_width)
            """
            cv2.namedWindow("cv2", cv2.WINDOW_NORMAL)        # Create a named window
            cv2.moveWindow("cv2", 40, 30)  # Move it to (40,30)
            cv2.imshow("cv2", img_with_overlay)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            """
            return img_with_overlay

         # Handle PIL images
        elif isinstance(image, PIL.Image.Image):
            # copy image
            img_with_overlay = copy.copy(image)
            # dims are reversed to conform with image drawing convention
            dims = ((self.box_br[1], self.box_br[0]), (self.box_tl[1], self.box_tl[0]))
            # get stroke width from image dimensions
            stroke_width = utilities.estimate_stroke_width(img_with_overlay.size)
            # instantiate Draw context
            shape_writer = PIL.ImageDraw.Draw(img_with_overlay)
            shape_writer.rectangle(dims, outline=colour, width=stroke_width)
            #img_with_overlay.show()
            return img_with_overlay


    def playback_history(self, image, save_path):
        """
        Generates an mp4 video of the box's location history
        Args:
            image: Image for box to be drawn on
            save_path: Video output path
        Returns:
        Raises:
        """
        # set up save path and temporary box object


        ### This should be uncommented if the file should be named as box_id
        # ##save_path = save_path + "/" + str(self._metadata.box_id) + ".avi"


        temp_box = Box(self.s_map, self._metadata.starting_box_tl, self._metadata.starting_dims, self._min_size)
        print("Saving video to : ", save_path)
        # initialise writer
        cv2.VideoWriter_fourcc(*'X264')
        writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'X264'), 1., (image.shape[1], image.shape[0]))
        
        # add starting position image
        for _ in range(3):
            writer.write(temp_box.overlay_box(image))
        # loop over history to generate images
        for vector in self._metadata.history:
            temp_box.transform(vector)
            writer.write(temp_box.overlay_box(image))
        # write end image for padding
        for _ in range(3):
            writer.write(temp_box.overlay_box(image))
        
        writer.release()

    def write_to_file(self, folderpath, imagepath, video_ext=".avi"):
        """
        Writes box + video + metadata to folderpath
        """
        # get image name from imagepath Path (remove file extension)
        image_name = imagepath.stem
        if self.metadata.construction_request is not None:
            request_name = self.metadata.construction_request[0] + "_"
        else:
            request_name = ""
        # build the file names
        outimg_path = folderpath / Path("boxed_" + request_name + str(image_name) + str(imagepath.suffix))
        outsmap_path = folderpath / Path("boxed_smap_" + request_name + str(image_name) + str(imagepath.suffix))
        outvid_path = folderpath / Path("history_" + request_name + str(image_name) + video_ext)
        metafile_path = folderpath / Path("metadata_" + request_name + str(image_name) + ".txt")

        # load image
        image = cv2.imread(str(imagepath))
        # write box image
        outimg = self.overlay_box(image)
        cv2.imwrite(str(outimg_path), outimg)
        # write box on smap
        outsmap = self.overlay_box(self._s_map)
        cv2.imwrite(str(outsmap_path), outsmap)

        # write video
        self.playback_history(image, str(outvid_path))

        # write metadata
        writefile = open(metafile_path, "w+")
        writefile.write(str(self.metadata.__dict__))
        writefile.close()

        

# ========================= /class ========================

import copy
import sys
def minimise_cost(starting_box, directions_list, step_size=10, n_iterations=10000):
    """
    Minimises the cost defined by the box class by exploring
    the saliency map space stored in the box.

    Args:
        starting_box: Box object located at the desired starting position of
                      the descent.
        step_size: number of pixels each movement should be (should this be a vector)
        n_iterations: number of iterations that the minimisation should go through (make this smarter)
        
        directions_list: Defines the possible moves that the box can make
                         including translation and resizing. Each direction is
                         2 2D vectors. First vector must be for translation,
                         second vector for resizing.
    Returns:
        optimum_box: This is the best box position according to the algorithm.
    Raises:
        
    """
    
    optimum_box = starting_box
    # loop over n iterations. Each iteration consists of constructing
    # boxes by moving the current box according to each direction in
    # direction list. The costs and corresponding direction is recorded
    # and the minimum cost is selected.
    for iteration in range(n_iterations):
        # create empty candidates list. Stores a list of dictionaries
        candidate_vectors = [np.array([[0, 0], [0, 0]])]
        # simple list of costs so we can easily find the minimum
        candidate_costs = [optimum_box.cost]
        # loop over all translations/transformations
        for vector in directions_list:
            #print("-------------new direction------------")
            # create new candidate box and move according to vector
            candidate_box = copy.copy(optimum_box)
            # try-except block to catch boxes drawn out of bounds
            try:
                candidate_box.transform(step_size * vector)
            except ValueError:
                # skip invalid boxes
                continue
            
            # check that box is valid
            # print(candidate_box.data)
            candidate_vectors.append(vector)
            candidate_costs.append(candidate_box.cost)

        # now we need to select the best candidate
        
        best_cost = min(candidate_costs)
        best_vector = candidate_vectors[candidate_costs.index(best_cost)]
        # add best cost to list of cost histories
        optimum_box.metadata.cost_history.append(best_cost)
        optimum_box.metadata.n_transformations += 1
        # check if best_vector is "no step made"
        if np.all(best_vector==0):
            print("Minimum found after", iteration + 1, "iterations")
            break

        # apply best transformation vector to optimum_box
        optimum_box.transform(step_size * best_vector, record_transformation=True)
        #print("Box ID: ", optimum_box.metadata.box_id)
        #print(best_vector)
        #print(best_cost)
    # Put optimum box printout here if necessary
    return optimum_box

import directions_factory
def main():
    """
    For testing only.
    """
    # load image
    image = cv2.imread(r'D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S7\MPhys\test_images\delpotro.jpg', 0)
    y = image.shape[0]
    x = image.shape[1]
    starting_box = Box(image, np.array([220, 440]), np.array([100, 100]), np.array([60, 60]))
   
   # print(starting_box.box_br)
    directions_list = directions_factory.unconstrained()

    lowest_cost_box = minimise_cost(starting_box, directions_list, 50, 70)
    
    print(type(image))

   # lowest_cost_box.write_to_file(Path("../mphys-testing/images/output/testingwrite/"), Path("../mphys-testing/images/birds.jpg"))
   
   # cv2.imshow("box", lowest_cost_box.overlay_box(image))
   # print(lowest_cost_box._metadata.history)

   # lowest_cost_box.playback_history(cv2.imread("../mphys-testing/images/birds.jpg", 0), '../mphys-testing/salience-in-photographs/images/output')
   # cv2.waitKey(0)

if __name__ == "__main__":
    main()
