import cv2
import numpy as np
import matplotlib.pyplot as plt


# returns salience map of an image
def getSalience(image):

    # initialize OpenCV's static saliency spectral residual detector and
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()

    # compute the saliency map
    _, saliencyMap = saliency.computeSaliency(image)

    # convert from 0-1 to 0-255
    saliencyMap = (saliencyMap * 255).astype("uint8")

    return saliencyMap


# load the input image (in greyscale)
image = cv2.imread('Images/footballer.jpg', 0)

# get a salience map of the image
salienceMap = getSalience(image)

# fourier transform
f = np.fft.fft2(image)

# shift each pixel so low frequency is in the center
fshift = np.fft.fftshift(f)

# magnitude spectrum (also: complex -> real number, abs())
magnitude_spectrum = 20 * np.log(np.abs(fshift))

# remove low frequencies
rows, cols = image.shape
crow,ccol = int(rows/2) , int(cols/2)
fshift[crow-30:crow+30, ccol-30:ccol+30] = 0

# undo the shift
f_ishift = np.fft.ifftshift(fshift)

# inverse fourier
img_back = np.fft.ifft2(f_ishift)

# complex -> real number
img_back = np.abs(img_back)

# need to ensure that array elements are encoded as uint8
# to work with cv2.imshow()
img_back = np.array(img_back, dtype=np.uint8)

# show using matplotlib
plt.imshow(img_back, cmap='gray')

# show using opencv
cv2.imshow("Should be the same", img_back)

plt.show()
cv2.waitKey(0)

