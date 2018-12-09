"""
--Naim Sen--
--Toby Ticehurst--

box_factory.py

for creating template starting boxes
"""


class BoxFactory(object):
    """
    BoxFactory encapsulates all template generation of the
    box. Should be able to create multiple boxes .
    """

    def __init__(self, s_map, text=None):
        self._s_map = s_map
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
        pos_readable = request_readable[0]
        dims_readable = request_readable[1]

        
         

    def load_requests(self, requests_readable):
        self._requests_list = []

    

