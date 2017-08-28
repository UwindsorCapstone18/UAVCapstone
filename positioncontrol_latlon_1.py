import dronekit as dk
import time
import numpy as np
import os
from matplotlib import pylab as pl
import decimal
##from geopy.distance import vincenty
import cv2
import RPi.GPIO as GPIO
import sonarlib

vehicle = dk.connect('/dev/ttyS0', baud=57600, heartbeat_timeout=20)

x1 = 1498
x2 = 1515
x4 = 1499
aalt = []

allposition = []
cap0 = cv2.VideoCapture(0)
######################################################
# Set the Sonar
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(0.1)
################################################
# Armed and Takeoff
print "Arming motors"
vehicle.mode = dk.VehicleMode("STABILIZE")
print vehicle.mode
vehicle.armed = True
time.sleep(2)
for h in range(0,8000):
    print vehicle.armed
time.sleep(3)
print "Taking off"
#######################################################

# Taking off PID Controller

original_altitude = sonarlib.distance(TRIG, ECHO)
last_altitude = sonarlib.distance(TRIG, ECHO)
integral_altitude = 0
altitude = sonarlib.distance(TRIG, ECHO)
print sonarlib.distance(TRIG, ECHO)
#######################################################
set_altitude = 0.5

# Coefficient of PID
Kp = 10
Ki = 0.5
Kd = 0.5
error = set_altitude - altitude

g = 1300
while True:
    vehicle.channels.overrides = {'1':x1, '2':x2, '3':g, '4':x4}
    print vehicle.channels.overrides
    takeoff_alt = sonarlib.distance(TRIG, ECHO)
    print takeoff_alt
    if takeoff_alt > 0.1:
        g = g-4
        break
    g = g + 3
    print g
    time.sleep(0.1)

# Position PID for TAKING OFF
set_lat = vehicle.location.global_frame.lat
set_lon = vehicle.location.global_frame.lon
set_latm = round((set_lat * 1000 - np.fix(set_lat * 1000)) * 100, 2)
set_lonm = round((set_lon * 1000 - np.fix(set_lon * 1000)) * 100, 2)
now_lat = vehicle.location.global_frame.lat
now_latm = round((now_lat * 100 - np.fix(now_lat * 100)) * 1000, 2)
now_lon = vehicle.location.global_frame.lon
now_lonm = round((now_lon * 100 - np.fix(now_lon * 100)) * 1000, 2)
original_latm = round((now_lat * 100 - np.fix(now_lat * 100)) * 1000, 2)
lat_dis = set_latm - now_latm
original_lonm = round((now_lon * 100 - np.fix(now_lon * 100)) * 1000, 2)
lon_dis = set_lonm - now_lonm
last_lat = 0
last_lon = 0
integral_lat = 0
integral_lon = 0
############################################################################################

# Coefficient of Position PID Controller during Taking Off
Kp_take = 1.5
Ki_take = 2
Kd_take = 0


for i in range(0, 200000):
    # Position PID control for TAKING OFF
    now_lat = vehicle.location.global_frame.lat
    now_lon = vehicle.location.global_frame.lon
    now_latm = round((now_lat * 1000 - np.fix(now_lat * 1000)) * 100, 2)
    now_lonm = round((now_lon * 1000 - np.fix(now_lon * 1000)) * 100, 2)
    error_lat = set_latm - now_latm
    error_lon = set_lonm - now_lonm
    delta_lat = error_lat - last_lat
    delta_lon = error_lon - last_lon
    last_lat = error_lat
    last_lon = error_lon
    if error_lat > 15 or error_lon < -15 or error_lon > 15 or error_lon < -15:
        vehicle.mode = dk.VehicleMode("LAND")
        time.sleep(0.5)
        exit()

    if i % 1500 == 0:
        integral_lat = error_lat + integral_lat
        integral_lon = error_lon + integral_lon

    b = 1515 - Kp_take * error_lat - Ki_take * integral_lat - Kd_take * delta_lat  # for ch2
    if b < 992:
        b = 992
    elif b > 2014:
        b = 2014
    #

    if c < 991:
        c = 991
    elif c > 2010:
        c = 2010
##########################################################################

    # Altitude PID controller
    altitude = sonarlib.distance(TRIG, ECHO)
    error = set_altitude - altitude
    delta_altitude = altitude - last_altitude
    last_altitude = altitude
    if i % 15000 == 0:
        integral_altitude = error + integral_altitude
    elif i % 100000 == 0:
        integral_altitude = 0
    a = g + Kp * error + Kd * delta_altitude + Ki * integral_altitude   # change Kd to be -
    if a <995:
        a = 995
    elif a > 2017:
        a = 2017
    vehicle.channels.overrides = {'1': c, '2': b, '3': a, '4': x4}  # wind speed is 10, dir is south 1625
    print vehicle.channels.overrides
    print altitude
    if altitude > 4.5:
        vehicle.mode = dk.VehicleMode("LAND")
        time.sleep(0.5)
        exit()
    print vehicle.location.global_frame

    aalt = np.append(aalt, altitude)
    if i >= 110000:
        if aalt[i] == aalt[i-500]:
            break
    time.sleep(0.2)
######################################################################################

# Mission Start
print "start go to target location"
with open('positions.txt','r') as f:
    for line in f:
        allposition.append(map(float,line.split(',')))
n = 0
while True:
    if n > 2:
        break
    alatdis = []
    alondis = []
    set_position = allposition[n]  # set position
    set_lat = set_position[0]                    # set latitude
    set_latm = round((set_lat * 10 - np.fix(set_lat * 10)) * 10000, 2)   # convert latitude in meters
    now_position = (vehicle.location.global_frame.lat, vehicle.location.global_frame.lon)
    now_lat = vehicle.location.global_frame.lat
    now_latm = round((now_lat * 10 - np.fix(now_lat * 10)) * 10000, 2)  # convert now latitude in meter
    original_latm = round((now_lat * 10 - np.fix(now_lat * 10)) * 10000, 2)
    lat_dis = set_latm - now_latm

    set_lon = set_position[1]                    # set longitude
    set_lonm = round((set_lon * 10 - np.fix(set_lon * 10)) * 10000, 2)   # convert longitude in meters
    now_lon = vehicle.location.global_frame.lon
    now_lonm = round((now_lon * 10 - np.fix(now_lon * 10)) * 10000, 2)   # convert now longitude in meter
    original_lonm = round((now_lon * 10 - np.fix(now_lon * 10)) * 100, 2)
    lon_dis = set_lonm - now_lonm

    last_lat = now_lat                            # last latitude for Kd
    last_lon = now_lon                            # last longitude for Kd

    integral_lat = 0         # integral latitude for Ki
    integral_lon = 0         # integral longitude for Ki

    # Keep Longitude when move latitude
    keep_lon = vehicle.location.global_frame.lon
    keep_lonm = round((keep_lon * 10 - np.fix(keep_lon * 10)) * 10000, 2)

    # Kp ,Ki and Kd for the Latitude Movement
    Kp_lat = 50
    Ki_lat = 0.5
    Kd_lat = 15
    Ki_lat1 = 0

    # Kp, Ki, and Kd for keep latitude and longitude
    Kp_keep = 5
    Ki_keep = 0.5
    Kd_keep = 0

    alat = []
    alon = []
####################################################################################

    # Latitude PID control
    for j in range(300000):
        # Keep Altitude PID
        altitude = sonarlib.distance(TRIG, ECHO)
        error = set_altitude - altitude
        delta_altitude = altitude - last_altitude
        last_altitude = altitude
        if j % 15000 == 0:
            integral_altitude = error + integral_altitude
        elif j % 100000 == 0:
            integral_altitude = 0
        a = g + Kp * error + Kd * delta_altitude + Ki * integral_altitude
        if a < 995:
            a = 995
        elif a > 2017:
            a = 2017
        ##################################################################

        # Keep Longitude PID
        now_lon = vehicle.location.global_frame.lon
        now_lonm = round((now_lon * 10 - np.fix(now_lon * 10)) * 10000, 2)
        error_lon = keep_lonm - now_lonm
        delta_lon = now_lonm - last_lon
        last_lon = now_lonm

        if j % 2000 == 0:
            integral_lon = error_lon + integral_lon
        c = round(1498 + Kp_keep * error_lon + Ki_keep * integral_lon + Kd_keep * delta_lon, 1)
        if c < 991:
            c = 991
        elif c > 2010:
            c = 2010
        ######################################################################
        # Latitude Position PID

        now_lat = vehicle.location.global_frame.lat
        now_latm = round((now_lat * 10 - np.fix(now_lat * 10)) * 10000, 2)
        alat = np.append(alat, now_latm)
        lat_avg = now_latm
        if j >= 4:
            lat_avg = (alat[j - 4] + alat[j - 3] + alat[j - 2] + alat[j - 1] + alat[j]) / 5


        error_lat = set_latm - lat_avg

        delta_lat = lat_avg - last_lat

        last_lat = lat_avg

        if j % 1000 == 0:
            integral_lat = error_lat + integral_lat

        b = round(1515 - Kp_lat * error_lat - Ki_lat * integral_lat - Kd_lat * delta_lat, 1)  # it was -
        if b < 992:
            b = 992
        elif b > 2010:
            b = 2010
        vehicle.channels.overrides = {'1': c, '2': b, '3': a, '4': x4}

        lat_dis = set_latm - lat_avg

        print "lat_dis is %s" % lat_dis
        print vehicle.channels.overrides
        alatdis = np.append(alatdis, lat_dis)
        if j > 100000:
            if np.abs(alatdis[j]) < 3 and np.abs(alatdis[j] - alatdis[j - 1000]) < 0.5:
                print "arrive set latitude"
                break
        elif j > 30000 and np.abs(lat_dis) > 50:
            vehicle.mode = dk.VehicleMode("LAND")
        if lat_avg > 7959.10 or lat_avg < 7779.60 or now_lonm < -6922.30 or now_lonm > -6833.10:
            while True:
                vehicle.channels.overrides = {'1': x1, '2': x2, '3': 995, '4': x4}
                vehicle.mode = dk.VehicleMode("LAND")
                time.sleep(0.5)
                exit()
        time.sleep(0.2)
    ############################################################################################
    #  Keep Latitude
    keep_lat = vehicle.location.global_frame.lat
    keep_latm = round((keep_lat * 10 - np.fix(keep_lat * 10)) * 10000, 2)
    last_lat = keep_latm
    integral_lat = 0

    # Longitude PID control
    for k in range(0, 300000):
        # Keep Altitude PID
        altitude = sonarlib.distance(TRIG, ECHO)
        error = set_altitude - altitude
        delta_altitude = altitude - last_altitude
        last_altitude = altitude
        if k % 15000 == 0:
            integral_altitude = error + integral_altitude
        elif k % 100000 == 0:
            integral_altitude = 0
        a = g + Kp * error + Kd * delta_altitude + Ki * integral_altitude
        if a < 995:
            a = 995
        elif a > 2017:
            a = 2017
        # Keep Latitude PID
        now_lat = vehicle.location.global_frame.lat
        now_latm = round((now_lat * 10 - np.fix(now_lat * 10)) * 10000, 2)
        error_lat = keep_latm - now_latm
        delta_lat = now_latm - last_lat
        last_lat = now_latm

        if k % 2000 == 0:
            integral_lat = error_lat + integral_lat
        b = round(1515 - Kp_keep * error_lat - Ki_keep * integral_lat - Kd_keep * delta_lat, 1)
        if b < 992:
            b = 992
        elif b > 2014:
            b = 2014
        # Longitude PID
        now_lon = vehicle.location.global_frame.lon
        now_lonm = round((now_lon * 10 - np.fix(now_lon * 10)) * 10000, 2)
        alon = np.append(alon, now_lonm)
        lon_avg = now_lonm
        if k >= 4:
            lon_avg = (alon[k - 4] + alon[k - 3] + alon[k - 2] + alon[k - 1] + alon[k]) / 5
        # print "lon avg is %s" % lon_avg

        error_lon = set_lonm - lon_avg
        delta_lon = lon_avg - last_lon
        last_lon = lon_avg
        if k % 2000 == 0:
            integral_lon = error_lon + integral_lon
        c = round(1498 + Kp_lat * error_lon + Ki_lat * integral_lon + Kd_lat * delta_lon, 1)  # was +

        if c < 991:
            c = 991
        elif c > 2010:
            c = 2010
        vehicle.channels.overrides = {'1': c, '2': b, '3': a, '4': x4}
        lon_dis = set_lonm - lon_avg
        print "lon_dis is %s" % lon_dis
        print vehicle.channels.overrides
        alondis = np.append(alondis, lon_dis)
        if k > 100000:
            if np.abs(alondis[k]) < 4 and np.abs(alondis[k] - alondis[k - 1000]) < 0.5:
                print "arrive set longitude"
                cap = cv2.VideoCapture(0)
                cap.set(4, 800)
                cap.set(3, 600)
                for l in range(0,30):
                    vehicle.channels.overrides = {'1': x1, '2': x2, '3': g, '4': x4}
                    ret, frame = cap.read()
                    cv2.imwrite(os.path.join("/home/pi/dacha", 'position%d.png') % n, frame)
                    cv2.imshow('frame', frame)
                cap.release()
                cv2.destroyAllWindows()
                break

        elif k > 30000 and np.abs(lon_dis) > 50:
            vehicle.mode = dk.VehicleMode("LAND")
        if lat_avg > 7959.10 or lat_avg < 7779.60 or now_lonm < -6922.30 or now_lonm > -6833.10:
            while True:
                vehicle.channels.overrides = {'1': x1, '2': x2, '3': 995, '4': x4}
                vehicle.mode = dk.VehicleMode("LAND")
                time.sleep(0.5)
                exit()
        time.sleep(0.2)
    n = n + 1
j = j + 1
k = k + 1
print j
print k

vehicle.close()
