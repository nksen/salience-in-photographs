import argparse
import cv2
 
# load the input image (in colour)
image = cv2.imread('images/birds.jpg')

# initialize OpenCV's static saliency spectral residual detector and
saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
# compute the saliency map
success, saliencyMap = saliency.computeSaliency(image)
# convert from 0-1 to 0-255
saliencyMap = (saliencyMap * 255).astype("uint8")

# threshold of the saliency map 
# any pixel between 50 and 255 is made white and everything else black
retval, threshold = cv2.threshold(saliencyMap, 50, 255, cv2.THRESH_BINARY)

cv2.imshow("Image", image)
cv2.imshow("Output", saliencyMap)
cv2.imshow("Threshold", threshold)

cv2.waitKey(0)


