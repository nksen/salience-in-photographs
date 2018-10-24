import cv2
import numpy as np


# image assumed to be BGR or greyscale
def fourierAnalysis(image):

    # convert to greyscale if haven't already
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # fourier transform
    fourier = np.fft.fft2(image)

    # shift each pixel so low frequency is in the center
    shiftedFourier = np.fft.fftshift(fourier)

    # magnitude spectrum (also: complex -> real number, abs())
    magnitudeSpectrum = 20 * np.log(np.abs(shiftedFourier))

    # remove low frequencies
    rows, columns = image.shape
    rowCenter, columnCenter = int(rows / 2) , int(columns / 2)
    shiftedFourier[rowCenter - 30 : rowCenter + 30, columnCenter - 30 : columnCenter + 30] = 0

    # undo the shift
    newFourier = np.fft.ifftshift(shiftedFourier)

    # inverse fourier
    newImage = np.fft.ifft2(newFourier)

    # complex -> real number
    newImage = np.abs(newImage)

    # need to ensure that array elements are encoded as uint8
    # to work with cv2.imshow()
    newImage = np.array(newImage, dtype = np.uint8)

    return newImage

# get weird artifacting at the edge of images after the fourier analysis
def removeEdgeArtifacts(image, width):

    for i in range(0, width):

        image[i, :] = 0         # first rows to 0       
        image[-i - 1, :] = 0    # last rows    
        image[:, i] = 0         # first columns
        image[:, -i - 1] = 0    # last columns

    return image
