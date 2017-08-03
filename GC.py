import numpy as np
import cv2



### open the test image saved from test_9_selecting_colour.py
img = cv2.imread('geese.png',1)

### converting image to grey scale
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

### Thresholding the grey scale image
ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)


### noise removal using opening, you can modify the kernel and iterations
kernel = np.ones((1,1),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)


### closing the gaps in targets, you can modify the kernel and iterations, having a big kernel or high number of 
### iterations can join two targets together
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, np.ones((2,2),np.uint8),iterations=2)


### This is for grouping nearby targets as one object.
### fl, fl2 and fl3 are not used in this code.
### ctrs = centroids of targets
fl, fl2, fl3, ctrs = cv2.connectedComponentsWithStats(closing)


	
### Now we create a region of interest, ROI, for every target, or centroid.
### Obtain the area of every ROI and adding them to a vector called "vec"
vec = []
img = cv2.imread('geese.png',1)

for i in range(len(ctrs)):
	
	test = np.zeros((10,10,1), np.uint8)
	cv2.circle(img,(int(ctrs[i][0]),int(ctrs[i][1])), 2, (0,0,255), -1)
	x = int(ctrs[i][0])
	y = int(ctrs[i][1])
	test = closing[y-5:y+5, x-5:x+5, ]
	vectemp = []
	for j in range(10):
		vectemp.append(sum(test[j]))
	vec.append(sum(vectemp))


### Creating a safe, or threshold, area number. In this case it is 2000
safe = 2000
### Now we test every area and see if it passes the threshold.
### if it does we draw a green square and add that centroid to the vector called "count".
count = []
for i in range(len(ctrs)):

	x = int(ctrs[i][0])
	y = int(ctrs[i][1])
	
	test = closing[y-5:y+5, x-5:x+5, ]
	vectemp = []
	for j in range(10):
		vectemp.append(sum(test[j]))
	xd = sum(vectemp)
	if xd >= safe:
		cv2.rectangle(img,(x-5,y-5),(x+5,y+5),(5,255,0),0)
		count.append(120)
		


### show results
print  'Number of sheep = ' + str(len(count))
cv2.imshow('frame', img)
cv2.waitKey(0)
cv2.destroyAllWindows()




