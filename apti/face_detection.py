import cv2
import numpy as np
#import face_recognition


if __name__ == "__main__":

    # read in image (colour and grayscale needed)        
    image = cv2.imread(r"D:\Users\Naim\OneDrive\CloudDocs\UNIVERSITY\S8\MPhys_s8\test_images\alonso.jpg", 1)

    # openCV Method (1)
    face_cascade = cv2.CascadeClassifier(r"C:\Users\Naim\Source\Repos\salience-in-photographs\apti\cascades\haarcascade_frontalface_alt2.xml")

    # format is (top left x, top left y, width, height)
    face_locations_1 = face_cascade.detectMultiScale(image, scaleFactor=1.5, minNeighbors=5)

    print("Face Boxes (Method 1): ")

    for (x, y, w, h) in face_locations_1:

        # print the coords
        print(x, y, x + w, y + h)

        # draw the rectangle on the image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)


    """
    # Method 2
    # format is (top left y, top left x, bottom right y, bottom right x)
    face_locations_2 = face_recognition.face_locations(image)

    print("Face Boxes (Method 2): ")

    for (tl_y, tl_x, br_y, br_x) in face_locations_2:

        # print the coords
        print(tl_x, tl_y, br_x, br_y)

        # draw the rectangle on the image
        cv2.rectangle(image, (tl_x, tl_y), (br_x, br_y), (255, 0, 0), 3)


    """
    cv2.imshow("Faces", image)
    cv2.waitKey(0)
    


