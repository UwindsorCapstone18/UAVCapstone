import dronekit as dk
import time
import math
import numpy as np
import decimal
from matplotlib import pylab as pl
from getkey import getkey, keys
from geopy.distance import vincenty

vehicle = dk.connect('tcp:127.0.0.1:5760', baud=57600, heartbeat_timeout=20)

# Basic Parameters
z1 = 1499
z2 = 1517
z3 = 1220
z4 = 1506
array_altitude = []
array_latitude = []
array_lontitude = []
vehicle.channels.overrides = {'1': z1, '2': z2, '3': 992, '4': z4}

# Altitude Input
set_altitude = 1

# Armed and Takeoff
print "Arming motors"
vehicle.mode = dk.VehicleMode("STABILIZE")
print vehicle.mode
vehicle.armed = True
time.sleep(2)

# Save Original GPS
latitude_origin = vehicle.location.global_relative_frame.lat
lontitude_origin = vehicle.location.global_relative_frame.lon

for i in range(0, 8000):
    print vehicle.armed
time.sleep(2)
vehicle.channels.overrides = {'1': z1, '2': z2, '3': 992, '4': z4}
vehicle.channels.overrides = {'1': z1, '2': z2, '3': 1000, '4': z4}
time.sleep(1)
print "Taking off"

# Gain Altitude
for j in range(0, 200000):

    altitude = vehicle.location.global_relative_frame.alt
    error_altitude = set_altitude - altitude
    current_latitude = vehicle.location.global_relative_frame.lat
    current_lontitude = vehicle.location.global_relative_frame.lon
    error_latitude = current_latitude - latitude_origin
    error_lontitude = current_lontitude - (lontitude_origin)

    N_altitude = 1220
    R_altitude = N_altitude - math.exp(abs(error_altitude))
    D_altitude = N_altitude + math.exp(abs(error_altitude))
    D_latitude = latitude_origin - math.exp(abs(error_latitude))
    R_latitude = latitude_origin + math.exp(abs(error_latitude))
    L_lontitude = lontitude_origin - math.exp(abs(error_lontitude))
    R_lontitude = lontitude_origin + math.exp(abs(error_lontitude))

    if error_altitude > 0:
        vehicle.channels.overrides = {'1': z1, '2': z2, '3': D_altitude, '4': z4}
    else:
        vehicle.channels.overrides = {'1': z1, '2': z2, '3': R_altitude, '4': z4}
    print altitude
    array_altitude = np.append(array_altitude, altitude)

# Horizontal Adjust, Current GPS (42.3046647,-83.0617518)

    if error_latitude > 0 and error_lontitude > 0:   #NE
        vehicle.channels.overrides = {'1': L_lontitude, '2': R_latitude, '3': z3, '4': z4}
    elif error_latitude < 0 and error_lontitude > 0: #SE
        vehicle.channels.overrides = {'1': L_lontitude, '2': D_latitude, '3': z3, '4': z4}
    elif error_latitude > 0 and error_lontitude < 0: #NW
        vehicle.channels.overrides = {'1': R_lontitude, '2': R_latitude, '3': z3, '4': z4}
    elif error_latitude < 0 and error_lontitude < 0: #SW
        vehicle.channels.overrides = {'1': R_lontitude, '2': D_latitude, '3': z3, '4': z4}
    else:
        vehicle.channels.overrides = {'1': z1, '2': z2, '3': z3, '4': z4}
    print current_latitude
    array_latitude = np.

# print vehicle.channels.overrides
# np.savetxt('aalt2.txt', aalt)
x = np.arange(200000)

pl.figure(1)
line1 = pl.plot(x, array_altitude)
# pl.figure(2)
# line2 = pl.plot(x, array_yaw)
pl.show()
vehicle.close()