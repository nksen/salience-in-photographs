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
        self._img = image
        self._min_size = minimum_size
        # compute and check box_br
        box_br = np.add(box_tl, dims)
        if box_br[0] > image.shape[0] or box_br[1] > image.shape[1]:
            raise ValueError("Box drawn out of range.")
        else:
            self._box_br = box_br
        
        # grab data inside box from image
        # create numpy mask
        mask_i = np.arange(box_tl[0], box_br[0], 1).tolist()
        mask_j = np.arange(box_tl[1], box_br[1], 1).tolist()
        ixgrid = np.ix_(mask_i, mask_j)
        # assign data
        self._data = image[ixgrid]

        # declare metadata Bunch type
        self._metadata = utilities.Bunch(history=np.array([]))

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
    def image(self):
        return self._img

    @property
    def cost(self):
        """
        Calculates the cost bounded by the box.
        Changing to a more detailed calculation.
        """
        return np.sum(self._data)/(self.shape[0] * self.shape[1])

    @property
    def metadata(self):
        """
        Returns metadata Bunch
        Bunch has the following items:
    
        """
        return self._metadata

    # ~~ Methods ~~ #
    def _translate(self, vector):
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
        self = self.__init__(self.image, new_anchor, self.shape, self._min_size)

    def _resize(self, vector):
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
        self = self.__init__(self.image, self.box_tl, new_dims, self._min_size)

    def transform(self, vector):
        """
        Transforms the box according to the specified vector by
        calling the translate and resize methods

        Args:
            vector: Compound vector of shape 2x2. The first element is the
                    translation vector, and the second is the resize
                    vector.
        Returns:
            N/A: modifies self by calling resize and translate (consider returning
                 success flag if necessary?
        Raises:
        """
        self._translate(vector[0])
        self._resize(vector[1])
        # record box history (assumes that the translate and resize functions do not
        # contribute.
        self._metadata.history.append(vector)
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

        # define tuples for cv2.rectangle
        colour = (255, 0, 0)
        # cv2.rectangle requires corner co-ordinates to be in (x,y) not (i,j)
        # so indices are flipped.
        tl_tuple = tuple(np.flip(self._box_tl, 0))
        br_tuple = tuple(np.flip(self.box_br, 0))

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
            print("-------------new direction------------")
            # create new candidate box and move according to vector
            candidate_box = copy.copy(optimum_box)
            # try-except block to catch boxes drawn out of bounds
            try:
                # translate the box
                candidate_box._translate(step_size * vector[0])
            except ValueError as err:
                print(err)
                print("Box drawn out of bounds. Translation vector: ", vector)
                # skip invalid boxes
                continue

            # catch boxes drawn with non-positive shape
            try:
                candidate_box._resize(step_size * vector[1])
            except ValueError as err:
                print(err)
                print("Dims out of bounds. Transformation vector: ", vector)
                # skip invalid boxes
                continue
            
            # check that box is valid
            # print(candidate_box.data)
            candidate_vectors.append(vector)
            candidate_costs.append(candidate_box.cost)
            

        # now we need to select the best candidate
        best_cost = min(candidate_costs)
        best_vector = candidate_vectors[candidate_costs.index(best_cost)]

        print(best_vector)
        print(best_cost)

        # apply best transformation vector to optimum_box
        optimum_box._translate(step_size * best_vector[0])
        optimum_box._resize(step_size * best_vector[1])

    return optimum_box



import directions_factory
if __name__ == "__main__":
    """
    For testing only.
    """
    # load image
    image = cv2.imread("../mphys-testing/salience-in-photographs/images/birds_salience_map.jpg", 0)
    y = image.shape[0]
    x = image.shape[1]
    starting_box = Box(image, np.array([y-100, x-100]), np.array([100, 100]), np.array([60, 60]))
    print(starting_box.box_br)
    directions_list = directions_factory.bottom_anchored()

    lowest_cost_box = minimise_cost(starting_box, 10, 70, directions_list)

    cv2.imshow("box", lowest_cost_box.overlay_box(lowest_cost_box.image))
    print(lowest_cost_box.shape)
    cv2.waitKey(0)
