##### Suggested clean drone startup sequence #####
import time, sys
import cv2
import numpy as np
import ps_drone                                    # Import PS-Drone-API

contourArray = []

drone = ps_drone.Drone()                           # Start using drone
drone.startup()                                    # Connects to drone and starts subprocesses

drone.reset()                                      # Sets drone's status to good
drone.setSpeed(0.05)
while (drone.getBattery()[0]==-1): time.sleep(0.1) # Wait until drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"% "+str(drone.getBattery()[1]) # Battery-status
drone.useDemoMode(True)                            # Set 15 basic dataset/sec

##### Mainprogram begin #####
drone.setConfigAllID()                              # Go to multiconfiguration-mode
drone.sdVideo()                                     # Choose lower resolution (try hdVideo())
drone.frontCam()                                    # Choose front view
CDC = drone.ConfigDataCount
while CDC==drone.ConfigDataCount: time.sleep(0.001) # Wait until it is done (after resync)
drone.startVideo()                                  # Start video-function
#drone.showVideo()                                   # Display the video

##### And action !
IMC = drone.VideoImageCount # Number of encoded videoframes


drone.trim()                                                     # Recalibrate sensors
drone.getSelfRotation(5)

print "Auto-alternation: "+str(drone.selfRotation)+" dec/sec"    # Showing value for auto-alteration

drone.takeoff()                                                  # Fly, drone, fly !
while drone.NavData["demo"][0][2]:     time.sleep(0.1)           # Wait until the drone is really flying (not in landed-mode anymore)

##### Mainprogram begin #####
print "Drone is flying now"



# contour filter
def is_contour_bad(c):
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
	# the contour is 'bad' if it is not a circle
	return not len(approx) == 4


while True:
    while drone.VideoImageCount==IMC: time.sleep(0.01) # Wait until the next video-frame
    IMC = drone.VideoImageCount
    img = drone.VideoImage
    frame = cv2.resize(img,(720,480))
    blur = cv2.GaussianBlur(frame, (5,5),0)

    #set marker
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([42, 63, 60])
    upper_green = np.array([179,255,227])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_green = cv2.erode(mask_green, None, iterations=2)
    mask_green = cv2.dilate(mask_green, None, iterations=2)

    
    # 	find contours in the bmask
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2. threshold(gray, 127, 255, 0)
    cnts = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    for w in cnts:
        if cv2.contourArea(w) < 1000:
            print "no good"
            continue
        c = max(cnts, key=cv2.contourArea)
        ob = cv2.moments(c)
        m00 = ob['m00']
        wX, wY = None, None
        if m00 !=0:
            wX = int(ob["m10"] / ob["m00"])
            wY = int(ob["m01"] / ob["m00"])
			
        ctr = (-1,-1)
		
        if wX != None and wY != None:
            ctr = (wX, wY)

		# draw the contour and center of the shape on the image
        if is_contour_bad(w):
            cv2.drawContours(frame, [c], -1, (0, 0, 255), 1)
            cv2.circle(frame, (wX,wY), 7, (255, 255, 255), -1)
        ob = cv2.moments(c)
        print cv2.contourArea(w)
        
        #zone 1
        if wX > 300 and wX < 420 and wY > 180 and wY < 3000:
            if cv2.contourArea(w) < 10000:
                print 'forward'
                drone.moveForward()
            elif cv2.contourArea(w) > 40000:
                print 'backward'
                drone.moveBackward()
            else:
                print 'hovering'
                drone.hover()
        #zone 2
        elif wX > 120 and wX < 300 and wY > 180 and wY < 300:
            print ' move_left'
            drone.moveLeft()
        #zone 3
        elif wX > 420 and wX < 600 and wY > 180 and wY < 300:
            print 'move_right'
            drone.moveRight()
        #zone 4
        elif wX > 300 and wX < 420 and wY > 0 and wY < 180:
            print 'move_up'
            drone.moveUp()
        #zone 5
        elif wX > 300 and wX < 420 and wY > 300 and wY < 480:
            print 'move_down'
            drone.moveDown()
        #zone 6
        elif wX > 120 and wX < 300 and wY > 0 and wY < 180:
            print 'move_left/move_up'
            drone.moveLeftUp()
        #zone 7
        elif wX > 120 and wX <300 and wY > 300 and wY < 480:
            print 'move_left/move_down'
            drone.moveLeftDown()
        #zone 8
        elif wX > 420 and wX < 600 and wY > 0 and wY < 180:
            print 'move_right/move_up'
            drone.moveRightUp()
        #zone 9
        elif wX > 420 and wX < 600 and wY > 300 and wY < 480:
            print 'move_right/move_down'
            drone.moveRightDown()
        #zone 10 
        elif wX > 0 and wX < 120:
            if cv2.contourArea(w) < 30000:
                print 'turn_left'
                drone.turnLeft()
            else:
                print 'move_left'
                drone.moveLeft()
        elif wX > 600 and wX < 720:
            if cv2.contourArea(w) < 30000:
                print 'turn_right'
                drone.turnRight()
            else:
                print 'move_right'
                drone.moveRight()


        #if cv2.contourArea(w)<200:
         #   continue
        #if cv2.contourArea(w)>50000:
         #   continue
        #cv2.drawContours(frame, [w], -1, (0,255,0),3)
        #cv2.circle(frame, (wX,wY), 7, (255, 255, 255), -1)
        #ob = cv2.moments(mask_green)
        #print cv2.contourArea(w)
       # if cv2.contourArea(w)<30000 and cv2.contourArea(w)>1000 :
        



    xaxis1 = cv2.line(frame, (120, 300), (600, 300), (33, 59, 66), 2)
    xaxis2 = cv2.line(frame, (120, 180), (600, 180), (33, 59, 66), 2)
    yaxis1 = cv2.line(frame, (120, 0), (120, 480), (33, 59, 66), 2)
    yaxis2 = cv2.line(frame, (300, 0), (300, 480), (33, 59, 66), 2)
    yaxis3 = cv2.line(frame, (420, 0), (420, 480), (33, 59, 66), 2)
    yaxis4 = cv2.line(frame, (600, 0), (600, 480), (33, 59, 66), 2)
    cv2.imshow('Drones video',frame)			# Show processed video-image
    #cv2.imshow('Mask',mask_green)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        drone.stop()
        break



#drone.land()
capture.release()
cv2.destroyAllWindows()						
    
