# salience-in-photographs

University of Manchester MPhys project: automatic placement of headlines on images whilst avoiding salient regions.


## v1.0.0-alpha
Python and [OpenCV](https://pypi.org/project/opencv-python/) are used to find the optimum position and dimensions for a text-box based on minimising the obscured saliency.
The saliency map used is from the OpenCV saliency API [1] and follows the method outlined by Hou and Zhang [2]. This can be swapped out in the [preprocessing](preprocessing.py) module.


## References
[1]: G. Bradski, ‘The OpenCV Library’, Dr. Dobb’s Journal of Software Tools, 2000.

[2]: X. Hou and L. Zhang, ‘Saliency detection: A spectral residual approach’, in In IEEE Conference on Computer Vision and Pattern Recognition (CVPR07). IEEE Computer Society, 2007, pp. 1–8.

### License

Copyright © 2018, Naim Sen.\
This software is licensed under the terms of the GNU General Public License.

Please send enquiries to naim.k.sen@outlook.com.