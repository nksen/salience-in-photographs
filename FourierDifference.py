import cv2
import numpy as np


# load the input image (in greyscale)
image = cv2.imread('Images/birds.jpg', 0)

# gaussian blur of the image. kernel of (3, 3) or (5, 5) works best
imageGaussianBlur = cv2.GaussianBlur(image, (3, 3), 0)

# find the difference of the images in fourier space (complex numbers)
fourierDifference = np.fft.fft2(image) - np.fft.fft2(imageGaussianBlur)

# inverse fourier
newImage = np.fft.ifft2(fourierDifference)

# complex -> real number
newImage = np.abs(newImage)

### having issues with variable types, np.uint8 etc, with both showing using opencv and normalising between 0 and 255

# need to ensure that array elements are encoded as uint8
# to work with cv2.imshow()
newImage = np.array(newImage, dtype = np.uint8)

# normalise
newImage *= int(255 / np.amax(newImage))

# show image using opencv
cv2.imshow("Difference in Fourier Space", newImage)

cv2.waitKey(0)