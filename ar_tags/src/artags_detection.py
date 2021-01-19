import cv2 
import numpy as np 
from cv2 import aruco

def order_coordinates(pts):
    
    #Initialize an empty array to save to next values 
    coordinates = np.zeros((4, 2), dtype="int")

    s = pts.sum(axis=1)
    coordinates[0] = pts[np.argmin(s)]
    coordinates[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    coordinates[1] = pts[np.argmin(diff)]
    coordinates[3] = pts[np.argmax(diff)]

    return coordinates

image = cv2.imread('imageR1.png')
h,w = image.shape[:2]

image = cv2.resize(image,(int(w*0.7), int(h*0.7)))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Initialize the aruco Dictionary and its parameters 
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters =  aruco.DetectorParameters_create()

#Detect the corners and id's in the examples 
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

#First we need to detect the markers itself, so we can later work with the coordinates we have for each.
frame_markers = aruco.drawDetectedMarkers(image.copy(), corners, ids)

#Show the markers detected
cv2.imshow('markers',frame_markers)
cv2.waitKey(0)
cv2.destroyAllWindows()