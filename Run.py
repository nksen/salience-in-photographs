import cv2
import numpy as np
from FourierAnalysis import *


# load the input image (in greyscale)
image = cv2.imread('Images/footballer.jpg', 0)

# fourier analysis
imageFourier1 = fourierAnalysis(image)
threshold1 = cv2.threshold(imageFourier1, np.average(imageFourier1) + np.std(imageFourier1), 255, cv2.THRESH_BINARY)[1]

# show using opencv
cv2.imshow("Fourier analysis result", imageFourier1)
cv2.imshow("Fourier analysis result, threshold", threshold1)

# remove artifacts
imageFourier2 = removeEdgeArtifacts(imageFourier1, 5)
threshold2 = cv2.threshold(imageFourier2, np.average(imageFourier2) + np.std(imageFourier2), 255, cv2.THRESH_BINARY)[1]

# show using opencv
cv2.imshow("Fourier analysis result, with edge artifacts removed", imageFourier2)
cv2.imshow("Fourier analysis result, with edge artifacts removed, threshold", threshold2)

cv2.waitKey(0)