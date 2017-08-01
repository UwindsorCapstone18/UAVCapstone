import dronekit as dk
import time
import numpy as np
from matplotlib import pylab as pl
import decimal
from geopy.distance import vincenty
import cv2

vehicle = dk.connect('tcp:127.0.0.1:5763', baud=57600, heartbeat_timeout=20)

x = 1500
aalt = []
alatdis = []
alondis = []
vehicle.channels.overrides = {'1': x, '2': x, '3': 1000, '4': x}
cap0 = cv2.VideoCapture(0)


# Armed and Takeoff
print "Arming motors"
vehicle.mode = dk.VehicleMode("STABILIZE")
print vehicle.mode
vehicle.armed = True
time.sleep(2)
for h in range(0,8000):
    print vehicle.armed
time.sleep(2)
vehicle.channels.overrides = {'1':x, '2':x, '3':1000, '4':x}
vehicle.channels.overrides = {'1':x, '2':x, '3':1010, '4':x}
time.sleep(1)
print "Taking off"
#######################################################################

# Altitude PID
for g in range(0, 100):
    original_altitude = vehicle.location.global_relative_frame.alt
    last_altitude = vehicle.location.global_relative_frame.alt
    integral_altitude = 0
    altitude = vehicle.location.global_relative_frame.alt
    print vehicle.location.global_relative_frame.alt
set_altitude = 20
# set_altitude = float(set_altitude)
Kp = 5
Ki = 0.5
Kd = 0.5
error = set_altitude - altitude
###########################################################################

# Position PID for TAKING OFF
set_lat = vehicle.location.global_relative_frame.lat
set_lon = vehicle.location.global_relative_frame.lon
set_latm = round((set_lat * 1000 - np.fix(set_lat * 1000)) * 100, 2)
set_lonm = round((set_lon * 1000 - np.fix(set_lon * 1000)) * 100, 2)
now_lat = vehicle.location.global_relative_frame.lat
now_latm = round((now_lat * 100 - np.fix(now_lat * 100)) * 1000, 2)
now_lon = vehicle.location.global_relative_frame.lon
now_lonm = round((now_lon * 100 - np.fix(now_lon * 100)) * 1000, 2)
original_latm = round((now_lat * 100 - np.fix(now_lat * 100)) * 1000, 2)
lat_dis = set_latm - now_latm
original_lonm = round((now_lon * 100 - np.fix(now_lon * 100)) * 1000, 2)
lon_dis = set_lonm - now_lonm
last_lat = 0
last_lon = 0
integral_lat = 0
integral_lon = 0

Kp_take = 2
Ki_take = 1
Kd_take = 0
# # calculate the angle between lat and lon
# if lon_dis == 0:
#     theta = 1.5708
# else:
#     theta = np.arctan(lat_dis/lon_dis)

for i in range(0, 200000):
    # Position PID control for TAKING OFF
    now_lat = vehicle.location.global_relative_frame.lat
    now_lon = vehicle.location.global_relative_frame.lon
    now_latm = round((now_lat * 1000 - np.fix(now_lat * 1000)) * 100, 2)
    now_lonm = round((now_lon * 1000 - np.fix(now_lon * 1000)) * 100, 2)
    error_lat = set_latm - now_latm
    error_lon = set_lonm - now_lonm
    delta_lat = error_lat - last_lat
    delta_lon = error_lon - last_lon
    last_lat = error_lat
    last_lon = error_lon

    if i % 15000 == 0:
        integral_lat = error_lat + integral_lat
        integral_lon = error_lon + integral_lon

    b = 1500 - Kp_take * error_lat - Ki_take * integral_lat - Kd_take * delta_lat  # for ch2
    if b < 1000:
        b = 1000
    elif b > 2000:
        b = 2000

    c = 1500 + Kp_take * error_lon + Ki_take * integral_lon + Kd_take * delta_lon
    if c < 1000:
        c = 1000
    elif c > 2000:
        c = 2000

    altitude = vehicle.location.global_relative_frame.alt
    error = set_altitude - altitude
    delta_altitude = altitude - last_altitude
    last_altitude = altitude
    if i % 15000 == 0:
        integral_altitude = error + integral_altitude
    elif i % 100000 == 0:
        integral_altitude = 0
    a = 1510 + Kp * error + Kd * delta_altitude + Ki * integral_altitude   # change Kd to be -
    if a <1000:
        a = 1000
    elif a > 2000:
        a = 2000
    vehicle.channels.overrides = {'1': c, '2': b, '3': a, '4': x}  # wind speed is 10, dir is south 1625
    print vehicle.channels.overrides
    print altitude
    print vehicle.location.global_relative_frame
    # print vehicle.location.global_relative_frame
    aalt = np.append(aalt, altitude)
    if i >= 110000:
        if aalt[i] == aalt[i-500]:
            break
########################################################################

print "start go to target location and Hovering"


set_position = (42.2793230, -83.0684440)  # set position
set_lat = 42.2803230                     # set latitude
set_latm = round((set_lat * 10 - np.fix(set_lat * 10)) * 10000, 2)   # convert latitude in meters
now_position = (vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon)
now_lat = vehicle.location.global_relative_frame.lat
now_latm = round((now_lat * 10 - np.fix(now_lat * 10)) * 10000, 2)  # convert now latitude in meter
original_latm =  round((now_lat * 10 - np.fix(now_lat * 10)) * 10000, 2)
lat_dis = set_latm - now_latm

set_lon = -83.0694440                     # set longitude
set_lonm = round((set_lon * 10 - np.fix(set_lon * 10)) * 10000, 2)   # convert longitude in meters
now_lon = vehicle.location.global_relative_frame.lon
now_lonm = round((now_lon * 10 - np.fix(now_lon * 10)) * 10000, 2)   # convert now longitude in meter
original_lonm = round((now_lon * 10 - np.fix(now_lon * 10)) * 100, 2)
lon_dis = set_lonm - now_lonm
# calculate the angle between lat and lon
if lon_dis == 0:
    theta = 1.5708
else:
    theta = np.arctan(lat_dis/lon_dis)
print theta

last_lat = now_lat                            # last latitude for Kd
last_lon = now_lon                            # last longitude for Kd

integral_lat = 0         # integral latitude for Ki
integral_lon = 0         # integral longitude for Ki

# Kp ,Ki and Kd for the latitude movement
Kp_lat = 2
Ki_lat = 0.1
Kd_lat = 1
Ki_lat1 = 0



alat = []
alon = []

for j in range(300000):
    # Keep Altitude PID
    altitude = vehicle.location.global_relative_frame.alt
    error = set_altitude - altitude
    delta_altitude = altitude - last_altitude
    last_altitude = altitude
    if j % 15000 == 0:
        integral_altitude = error + integral_altitude
    elif j % 100000 == 0:
        integral_altitude = 0
    a = 1510 + Kp * error + Kd * delta_altitude + Ki * integral_altitude
    if a < 1000:
        a = 1000
    elif a > 2000:
        a = 2000
    ##############################################################################

    # Position Pid
    now_lat = vehicle.location.global_relative_frame.lat
    now_latm =round((now_lat * 10 - np.fix(now_lat * 10)) * 10000, 2)
    alat = np.append(alat, now_latm)
    lat_avg = now_latm
    if j >= 4:
        lat_avg = (alat[j-4] + alat[j-3] + alat[j-2] + alat[j-1] + alat[j]) / 5
    print "lat avg is %s" % lat_avg
    now_lon = vehicle.location.global_relative_frame.lon
    now_lonm = round((now_lon * 10 - np.fix(now_lon * 10)) * 10000, 2)
    alon = np.append(alon, now_lonm)
    lon_avg = now_lonm
    if j >= 4:
        lon_avg = (alon[j-4] + alon[j-3] + alon[j-2] + alon[j-1] + alon[j]) / 5
    print "lon avg is %s" % lon_avg
    error_lat = set_latm - lat_avg
    error_lon = set_lonm - lon_avg
    delta_lat = lat_avg - last_lat
    delta_lon = lon_avg - last_lon
    last_lat = lat_avg
    last_lon = lon_avg
    integral_lat = error_lat + integral_lat
    integral_lon = error_lon + integral_lon
    if error_lon == 0:
        theta = 1.5708

        # PID calculation for ch2 latitude should - because 992 is forward
        if error_lat > -20 and error_lat < 20:
            b = round(1500 - Kp_lat * error_lat - Ki_lat * integral_lat - Kd_lat * delta_lat, 1)
            if b < 1000:
                b = 1000
            elif b > 2000:
                b = 2000
            c = round(1500 + Kp_lat * error_lon + Ki_lat * integral_lon + Kd_lat * delta_lon, 1)  # was +
            print "c is %s" % c
            if c < 1000:
                c = 1000
            elif c > 2000:
                c = 2000
            vehicle.channels.overrides = {'1': c, '2': b, '3': a, '4': x}
        elif error_lon < 20 and error_lon > -20:
            b = round(1500 - Kp_lat * error_lat - Ki_lat * integral_lat - Kd_lat * delta_lat, 1)
            if b < 1000:
                b = 1000
            elif b > 2000:
                b = 2000
            c = round(1500 + Kp_lat * error_lon + Ki_lat * integral_lon + Kd_lat * delta_lon, 1)
            if c < 1000:
                c = 1000
            elif c > 2000:
                c = 2000
            vehicle.channels.overrides = {'1': c, '2': b, '3': a, '4': x}
        else:
            b = round(1500 - Kp_lat * error_lat - Ki_lat * integral_lat - Kd_lat * delta_lat, 1)  # it was -
            if b < 1000:
                b = 1000
            elif b > 2000:
                b = 2000
            c = round(1500 + np.tan(theta_abs) * (Kp_lat * error_lat + Ki_lat * integral_lat + Kd_lat * delta_lat), 1)
            if c < 1000:
                c = 1000
            elif c > 2000:
                c = 2000
            vehicle.channels.overrides = {'1': c, '2': b, '3': a, '4': x}
    else:
        theta = np.arctan(error_lat / error_lon)
        theta_abs = np.absolute(theta)
        if theta_abs < 45:                                           # lon is the main
            if error_lat < 20 and error_lat > -20:
                # integral_lat = error_lat + integral_lat
                # integral_lon = error_lon + integral_lon
                b = round(1500 - Kp_lat * error_lat - Ki_lat * integral_lat - Kd_lat * delta_lat, 1)
                if b < 1000:
                    b = 1000
                elif b > 2000:
                    b = 2000
                c = round(1500 + Kp_lat * error_lon + Ki_lat * integral_lon + Kd_lat * delta_lon, 1)  # was +
                print "c is %s" % c
                if c < 1000:
                    c = 1000
                elif c > 2000:
                    c = 2000
                vehicle.channels.overrides = {'1': c, '2': b, '3': a, '4': x}
            elif error_lon < 20 and error_lon > -20:
                b = round(1500 - Kp_lat * error_lat - Ki_lat * integral_lat - Kd_lat * delta_lat, 1)
                if b < 1000:
                    b = 1000
                elif b > 2000:
                    b = 2000
                c = round(1500 + Kp_lat * error_lon + Ki_lat * integral_lon + Kd_lat * delta_lon, 1)
                if c < 1000:
                    c = 1000
                elif c > 2000:
                    c = 2000
                vehicle.channels.overrides = {'1': c, '2': b, '3': a, '4': x}
            else:
                b = round(1500 - np.tan(theta) * (Kp_lat * error_lon + Ki_lat * integral_lon + Kd_lat * delta_lon), 1)  # it was -
                if b < 1000:
                    b = 1000
                elif b > 2000:
                    b = 2000
                c = round(1500 + Kp_lat * error_lon + Ki_lat * integral_lon + Kd_lat * delta_lon, 1)
                if c < 1000:
                    c = 1000
                elif c > 2000:
                    c = 2000
                vehicle.channels.overrides = {'1': c, '2': b, '3': a, '4': x}
        elif theta_abs >= 45:                                            # lat is the main
            if error_lat < 20 and error_lat > -20:
                b = round(1500 - Kp_lat * error_lat - Ki_lat * integral_lat - Kd_lat * delta_lat, 1)
                if b < 1000:
                    b = 1000
                elif b > 2000:
                    b = 2000
                c = round(1500 + Kp_lat * error_lon + Ki_lat * integral_lon + Kd_lat * delta_lon, 1)  # was +
                print "c is %s" % c
                if c < 1000:
                    c = 1000
                elif c > 2000:
                    c = 2000
                vehicle.channels.overrides = {'1': c, '2': b, '3': a, '4': x}
            elif error_lon < 20 and error_lon > -20:
                b = round(1500 - Kp_lat * error_lat - Ki_lat * integral_lat - Kd_lat * delta_lat, 1)
                if b < 1000:
                    b = 1000
                elif b > 2000:
                    b = 2000
                c = round(1500 + Kp_lat * error_lon + Ki_lat * integral_lon + Kd_lat * delta_lon, 1)
                if c < 1000:
                    c = 1000
                elif c > 2000:
                    c = 2000
                vehicle.channels.overrides = {'1': c, '2': b, '3': a, '4': x}
            else:
                b = round(1500 - Kp_lat * error_lat - Ki_lat * integral_lat - Kd_lat * delta_lat, 1)  # it was -
                if b < 1000:
                    b = 1000
                elif b > 2000:
                    b = 2000
                c = round(1500 + (1 / np.tan(theta)) * (Kp_lat * error_lat + Ki_lat * integral_lat + Kd_lat * delta_lat), 1)
                if c < 1000:
                    c = 1000
                elif c > 2000:
                    c = 2000
                vehicle.channels.overrides = {'1': c, '2': b, '3': a, '4': x}





    lat_dis = set_latm - lat_avg
    lon_dis = set_lonm - lon_avg
    print vehicle.channels.overrides
    print "latitude distance is: %s" %lat_dis
    print "longitude distance is: %s" %lon_dis

    alatdis = np.append(alatdis, lat_dis)
    alondis = np.append(alondis, lon_dis)



z = np.arange(300000)



pl.figure(1)
line1 = pl.plot(z, alatdis)
pl.figure(2)
line2 = pl.plot(z, alondis)
pl.show()


vehicle.close()