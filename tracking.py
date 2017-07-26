import libardrone 
import cv2
import numpy as np
import math
import time



capture = cv2.VideoCapture (0)
capture.set(3,720)
capture.set(4,480)

drone = libardrone.ARDrone()
time.sleep(5)


drone.takeoff()

drone.hover()


while True:


	ret,frame = capture.read()
	blur = cv2.GaussianBlur(frame, (11,11),0)


	# set the marker
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_green = np.array([90,130,131])    # 90, 90, 85
	upper_green = np.array([90,150,141])  #130, 250, 250
	mask_green = cv2.inRange(hsv, lower_green, upper_green)
	
	cnts = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

	for w in cnts:
	# compute the center of the contour
		ob = cv2.moments(mask_green)
		wX = int(ob["m10"] / ob["m00"])
		wY = int(ob["m01"] / ob["m00"])
 
#  		if cv2.contourArea(w)<500:
# 			continue	
		# draw the contour and center of the shape on the image
		cv2.drawContours(frame, [w], -1, (0, 0, 255), 1)
		cv2.circle(frame, (wX, wY), 7, (255, 255, 255), -1)

	ob = cv2.moments(mask_green)
	print cv2.contourArea(w)

# 	if ob['m00'] >= 10000: 
# 
# 		Nx = int(ob['m10']/ob['m00'])
# 		Ny = int(ob['m01']/ob['m00'])


# 		lx = float((Nx-cx))/720
# 		ly = float((Ny-cy))/240 
		
		# if cv2.contourArea(w)<30000 and cv2.contourArea(w)>1000 :
	if  (wX > 0 and wX < 240 and wY > 0 and wY < 160):       			# Turn Right
		print 'turn right'
		drone.turn_right()
	elif (wX > 480 and wX < 720 and wY > 0 and wY < 160):				# Turn Left
		print 'turn left'
		drone.turn_left()
	elif (wX > 240 and wX < 480 and wY > 0 and wY < 160):    			# Move Down
		print 'move down'
		drone.move_down()
	elif (wX > 0 and wX < 240 and wY > 160 and wY < 320):				# Move Right
		print 'move right'
		drone.move_right()
	elif (wX > 480 and wX < 720 and wY > 160 and wY < 320):				# Move Left
		print 'move left'
		drone.move_left()
	elif (wX > 0 and wX < 240 and wY > 320 and wY < 480): 				# Forward
		print 'forward'
		drone.move_forward()
	elif (wX > 480 and wX < 720 and wY > 320 and wY < 480):				# Backward
		print 'backward'
		drone.move_backward()
	elif (wX > 240 and wX < 480 and wY > 320 and wY < 480):				# Move Up
		print 'move up'
		drone.move_up()
	else:																# Hovering
		print 'hovering'
		drone.hover()


	# if  wY < 240 :
# 		print 'move down'
# 		drone.move(0,0,-0.3,0)
# 	elif wY > 240 :
# 		print 'move up'
# 		drone.move(0,0,0.3,0)
# 	else        :
# 		print 'y calibrated ' 
# 		print 'forward'
# 		drone.move(0,0.3,0,0)

# 		elif cv2.contourArea(w)>70000:
# 	if  (wX > 360 and wX <= 600) :
# 		print 'move left'
# 		drone.move(-0.3,0,0,0)
# 	elif (wX > 120 and wX < 360) :
# 		print 'move right'
# 		drone.move(0.3,0,0,0)
	# elif wX < 120:
	# 				print 'turn right'
	# 				drone.turn_right()
	# 			elif wX > 600:
	# 				print 'turn_left'
	# 				drone.turn_left()
	# else        :
# 		print 'x calibrated '
# 		print 'back'
# 		drone.move(0,-0.3,0,0)
# 	if  wY < 240 :
# 		print 'move down'
# 		drone.move(0,0,-0.3,0)
# 	elif wY > 240 :
# 		print 'move up'
# 		drone.move(0,0,0.3,0)
# 	else        :
# 		print 'y calibrated '
# 		print 'back'
# 		drone.move(0,-0.3,0,0)
# 	# else :
# 	if wX < 120:
# 		print 'turn right'
# 		drone.move(0,0,0,0.3)
# 	elif wX > 600:
# 		print 'turn_left'
# 		drone.move(0,0,0,-0.3)
# 	else:
# 		drone.hover()
# 		print 'hover'
			
	# 	print" "
	# 	print" "

    xaxis1 = cv2.line(frame, (120, 280), (600, 280), (33, 59, 66), 2)
    xaxis2 = cv2.line(frame, (120, 200), (600, 200), (33, 59, 66), 2)
    yaxis1 = cv2.line(frame, (120, 0), (120, 480), (33, 59, 66), 2)
    yaxis2 = cv2.line(frame, (320, 0), (320, 480), (33, 59, 66), 2)
    yaxis3 = cv2.line(frame, (400, 0), (400, 480), (33, 59, 66), 2)
    yaxis4 = cv2.line(frame, (600, 0), (600, 480), (33, 59, 66), 2)



# 	cv2.circle(frame,(cx,cy),17,(0,255,0),7)
	cv2.imshow('cool',frame)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break



drone.land()
# drone.reset()
# drone.halt()
capture.release()
cv2.destroyAllWindows()
