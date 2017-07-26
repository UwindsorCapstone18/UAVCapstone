import libardrone 
import cv2
import numpy as np
import math
import time


# contour filter
def is_contour_bad(c):
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
	# the contour is 'bad' if it is not a circle
	return not len(approx) == 4

# turn on camera
capture = cv2.VideoCapture (0)
capture.set(3,720)
capture.set(4,480)

drone = libardrone.ARDrone()
time.sleep(5)


drone.takeoff()

drone.hover()

# center lines of x_axis&y_axis
cx = 360
cy = 240

while True:


	ret,frame = capture.read()
	blur = cv2.GaussianBlur(frame, (5,5),0)


	# set the marker
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_green = np.array([40,70,70])
	upper_green = np.array([80,200,200])
	mask_green = cv2.inRange(hsv, lower_green, upper_green)
	mask_green = cv2.erode(mask_green, None, iterations=2)
	mask_green = cv2.dilate(mask_green, None, iterations=2)

# 	find contours in the bmask
	cnts = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

	for w in cnts:
	# compute the center of the contour
		ob = cv2.moments(mask_green)
		m00 = ob['m00']
		wX, wY = None, None
		if m00 !=0:
			wX = int(ob["m10"] / ob["m00"])
			wY = int(ob["m01"] / ob["m00"])
			
		ctr = (-1,-1)
		
		if wX != None and wY != None:
			ctr = (wX, wY)
 
 		if cv2.contourArea(w)>100:
			continue	
		# draw the contour and center of the shape on the image
			if is_contour_bad(w):
				cv2.drawContours(frame, [w], -1, (0, 0, 255), 1)
				cv2.circle(frame, (wX,wY), 7, (255, 255, 255), -1)


		ob = cv2.moments(mask_green)
		print cv2.contourArea(w)

# 	if ob['m00'] >= 10000: 
# 
# 		Nx = int(ob['m10']/ob['m00'])
# 		Ny = int(ob['m01']/ob['m00'])


# 		lx = float((Nx-cx))/720
# 		ly = float((Ny-cy))/240 
		
		if cv2.contourArea(w)<30000 and cv2.contourArea(w)>1000 :
			drone.move_forward()
			if  (wX > 360 and wX < 600) :
				print 'move left'
				drone.move(-0.3,0,0,0)
		
			elif (wX > 120 and wX < 360) :
				print 'move right'
				drone.move(0.3,0,0,0)
			# elif wX < 120:
		# 				print 'turn right'
		# 				drone.turn_right()
		# 			elif wX > 600:
		# 				print 'turn_left'
		# 				drone.turn_left()
			else        :
				print 'x calibrated '
				print 'forward'
				drone.move(0,0.3,0,0)


			if  wY < 240 :
				print 'move down'
				drone.move(0,0,-0.3,0)
			elif wY > 240 :
				print 'move up'
				drone.move(0,0,0.3,0)
			else        :
				print 'y calibrated ' 
				print 'forward'
				drone.move(0,0.3,0,0)

		elif cv2.contourArea(w)>70000:
			if  (wX > 360 and wX < 600) :
				print 'move left'
				drone.move(-0.3,0,0,0)
			elif (wX > 120 and wX < 360) :
				print 'move right'
				drone.move(0.3,0,0,0)
		# elif wX < 120:
		# 				print 'turn right'
		# 				drone.turn_right()
		# 			elif wX > 600:
		# 				print 'turn_left'
		# 				drone.turn_left()
			else        :
				print 'x calibrated '
				print 'back'
				drone.move(0,-0.3,0,0)
			if  wY < 240 :
				print 'move down'
				drone.move(0,0,-0.3,0)
			elif wY > 240 :
				print 'move up'
				drone.move(0,0,0.3,0)
			else        :
				print 'y calibrated '
				print 'back'
				drone.move(0,-0.3,0,0)
			# else :
			if wX < 120:
				print 'turn right'
				drone.move(0,0,0,0.3)
			elif wX > 600: 
				print 'turn_left'
				drone.move(0,0,0,-0.3)
		else:
			drone.hover()
			print 'hover'
			
	# 	print" "
	# 	print" "
	yaxis = cv2.line(frame, (120, 0), (120, 480), (33, 59, 66), 2)
	yaxis = cv2.line(frame, (360, 0), (360, 480), (33, 59, 66), 2)
	yaxis = cv2.line(frame, (600, 0), (600, 480), (33, 59, 66), 2)
	yaxis = cv2.line(frame, (0, 240), (720, 240), (33, 59, 66), 2)
# 	cv2.circle(frame,(cx,cy),17,(0,255,0),7)
	cv2.imshow('frame',frame)
	cv2.imshow('mask',mask_green)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break



drone.land()
# drone.reset()
# drone.halt()
capture.release()
cv2.destroyAllWindows()