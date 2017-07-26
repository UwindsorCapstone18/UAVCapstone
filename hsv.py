import cv2
import numpy as np

greenlower = np.uint8([[[76,100,65]]])
hsv_greenlower = cv2.cvtColor(greenlower, cv2.COLOR_BGR2HSV)
greenhigher = np.uint8([[[178,200,145]]])
hsv_greenhigher = cv2.cvtColor(greenhigher, cv2.COLOR_BGR2HSV)
print hsv_greenlower
print hsv_greenhigher
