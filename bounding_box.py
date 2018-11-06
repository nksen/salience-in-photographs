"""
--Naim Sen--
--Toby Ticehurst--
Oct 18

bounding_box.py

Box class and accompanying functions.
"""

import cv2
import numpy as np
import operator


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
    def __init__(self, image, box_tl, dims, minimum_size=np.array([0, 0])):
        """
        Box object initialiser
        Args:
            image: np.array grayscale saliency map which the box is
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

        # check that dimensions are large than minimum_size
        if dims[0] < minimum_size[0]:
            raise ValueError("i'th dimension is less than minimum size.")
        if dims[1] < minimum_size[1]:
            raise ValueError("j'th dimension is less than minimum size.")
        
        # assign vars
        self._box_tl = box_tl
        self._dims = dims
        self._img = image
        # grab data inside box from image
        # create numpy mask
        mask_i = np.arange(box_tl[0], box_tl[0]+dims[0], 1).tolist()
        mask_j = np.arange(box_tl[1], box_tl[1]+dims[1], 1).tolist()
        ixgrid = np.ix_(mask_i, mask_j)
        # _data should never really be changed
        self._data = image[ixgrid]

    # ~~ Properties ~~ #
    @property
    def box_tl(self):
        return self._box_tl
  
    @property
    def shape(self):
        return self._dims

    @property
    def data(self):
        return self._data

    @property
    def image(self):
        return self._img

    @property
    def cost(self):
        """
        Calculates the cost bounded by the box.
        Changing to a more detailed calculation.
        """
        return np.sum(self._data)/(self.shape[0] * self.shape[1])

    # ~~ Methods ~~ #
    def translate(self, vector):
        """
        Translates the box by the specified vector.

        Args:
            vector: Translation vector in (i,j).
        Returns:
            N/A: modifies self by calling __init__.
        Raises:
        
        """
        # new anchor point
        new_anchor = np.add(self.box_tl, vector)
        # construct a new box object
        self = self.__init__(self.image, new_anchor, self.shape)

    def resize(self, vector):
        """
        Resizes the box by the specified amount in each direction.

        Args:
            vector: Specifies the change in side length for each
                    dimension. Must be give in (i,j).
        Returns:
            N/A: modifies self by calling __init__.
        Raises:
        
        """
        new_dims = np.add(self.shape, vector)
        self = self.__init__(self.image, self.box_tl, new_dims)

    def overlay_box(self, image):
        """
        Overlays a blue box on the image provided (note, not on own
        image).
        Args:
            image: np.array of the image that the box is to be drawn
                   on.
        Returns:
            img_with_overlay: The image with the overlaid box.
        Raises:
        
        """
        # check if image is colour or greyscale
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        # should replace this with an accessor for each of
        # the box's 4 corners
        box_br = np.add(self._box_tl, self._dims)

        # define tuples for cv2.rectangle
        colour = (255, 0, 0)
        # cv2.rectangle requires corner co-ordinates to be in (x,y) not (i,j)
        # so indices are flipped.
        tl_tuple = tuple(np.flip(self._box_tl, 0))
        br_tuple = tuple(np.flip(box_br, 0))

        img_with_overlay = cv2.rectangle(image, tl_tuple, br_tuple, colour, 3)
        return img_with_overlay


import copy
import sys
def minimise_cost(starting_box, step_size, n_iterations, directions_list):
    """
    Minimises the cost defined by the box class by exploring
    the image space stored in the box.

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
        current_box: This is the best box position according to the algorithm.
    Raises:
        
    """
    
    current_box = starting_box
    # loop over n iterations. Each iteration consists of constructing
    # boxes by moving the current box according to each direction in
    # direction list. The costs and corresponding direction is recorded
    # and the minimum cost is selected.
    for iteration in range(n_iterations):
        # create empty candidates list. Stores a list of dictionaries
        candidate_vectors = [np.array([[0, 0], [0, 0]])]
        # simple list of costs so we can easily find the minimum
        candidate_costs = [current_box.cost]
        # loop over all translations/transformations
        for vector in directions_list:
            print("-------------new direction------------")
            # create new box and move according to vector
            new_box = copy.copy(current_box)
            # try-except block to catch boxes drawn out of bounds
            try:
                # translate the box
                new_box.translate(step_size * vector[0])
            except ValueError:
                print("Box drawn out of bounds. Translation vector: ", vector)
                # skip invalid boxes
                continue

            # catch boxes drawn with non-positive shape
            try:
                new_box.resize(step_size * vector[1])
            except ValueError:
                print("Dims out of bounds. Transformation vector: ", vector)
                # skip invalid boxes
                continue
            
            # check that box is valid
            # print(new_box.data)
            candidate_vectors.append(vector)
            candidate_costs.append(new_box.cost)
            

        # now we need to select the best candidate
        best_cost = min(candidate_costs)
        best_vector = candidate_vectors[candidate_costs.index(best_cost)]

        print(best_vector)
        print(best_cost)

        # apply best transformation vector to current_box
        current_box.translate(step_size * best_vector[0])
        current_box.resize(step_size * best_vector[1])

    return current_box


if __name__ == "__main__":
    """
    For testing only.
    """
    # load image
    image = cv2.imread("../mphys-testing/salience-in-photographs/images/birds_salience_map.jpg", 0)
    starting_box = Box(image, np.array([200, 55]), np.array([100, 10]), np.array([25, 25]))
    directions_list = np.array(
        [
            [[1, 0], [0, 0]],
            [[0, 1], [0, 0]],
            [[-1, 0], [0, 0]],
            [[0, -1], [0, 0]],
            [[0, 0], [1, 0]],
            [[0, 0], [0, 1]],
            [[0, 0], [-1, 0]],
            [[0, 0], [0, -1]]
        ])
    
    lowest_cost_box = minimise_cost(starting_box, 10, 0, directions_list)

    cv2.imshow("box", lowest_cost_box.overlay_box(lowest_cost_box.image))
    cv2.waitKey()
