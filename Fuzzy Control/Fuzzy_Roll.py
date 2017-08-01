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
z = 1472
array_roll = []
vehicle.channels.overrides = {'1': z, '2': z, '3': 992, '4': z}
# Current Longtitude(42.3046647,-83.0617518)

# Longtitude Input
set_Longtitude = -275.18

# roll Gears
N_roll = 1472

R1_roll = 1550        #N_roll + math.exp(1)
R2_roll = 1650        #R1_roll + math.exp(3)
R3_roll = 1750        #R1_roll + math.exp(4)
R4_roll = 1850        #R1_roll + math.exp(5)
R5_roll = 1950        #R1_roll + math.exp(6)

D1_roll = 1422        #N_roll - math.exp(1)
D2_roll = 1372        #D1_roll - math.exp(3)
D3_roll = 1322        #D1_roll - math.exp(4)
D4_roll = 1272        #D1_roll - math.exp(5)
D5_roll = 1222        #D1_roll - math.exp(6)

# Armed and Takeoff
print "Arming motors"
vehicle.mode = dk.VehicleMode("STABILIZE")
print vehicle.mode
vehicle.armed = True
time.sleep(2)
for i in range(0, 8000):
    print vehicle.armed
time.sleep(2)
vehicle.channels.overrides = {'1': z, '2': z, '3': 992, '4': z}
vehicle.channels.overrides = {'1': z, '2': z, '3': 1000, '4': z}
time.sleep(1)
print "Taking off"

# Gain roll
for m in range(0, 200000):

    current_longtitude = vehicle.location.global_relative_frame.lon
    current_longtitude = round((current_longtitude * 100 - np.fix(current_longtitude * 100)) * 1000, 2)
    error_longtitude = (set_longtitude - current_longtitude)*(float(100)/float(88))
    abs_error_longtitude = abs(error_longtitude)
    ratio_error_longtitude = float(error_longtitude) / float(set_longtitude)
    abs_ratio_error_longtitude = abs(ratio_error_longtitude)

    if abs_error_longtitude < 0.5 or abs_error_longtitude == 0.5:
        vehicle.channels.overrides = {'1': N_roll, '2': z, '3': N_altitude, '4': z}
    elif abs_error_longtitude > 0.5:
        if abs_ratio_error_longtitude > 0.7 or abs_ratio_error_longtitude == 0.7:
            vehicle.channels.overrides = {'1': D5_roll, '2': z, '3': N_altitude, '4': z}
        elif abs_ratio_error_longtitude > 0.5 or abs_ratio_error_longtitude == 0.5:
            vehicle.channels.overrides = {'1': D4_roll, '2': z, '3': N_altitude, '4': z}
        elif abs_ratio_error_longtitude > 0.3 or abs_ratio_error_longtitude == 0.3:
            vehicle.channels.overrides = {'1': D3_roll, '2': z, '3': N_altitude, '4': z}
        elif abs_ratio_error_longtitude > 0.15 or abs_ratio_error_longtitude == 0.15:
            vehicle.channels.overrides = {'1': D2_roll, '2': z, '3': N_altitude, '4': z}
        else:
            vehicle.channels.overrides = {'1': D1_roll, '2': z, '3': N_altitude, '4': z}
    else:
        if abs_ratio_error_longtitude > 0.7 or abs_ratio_error_longtitude == 0.7:
            vehicle.channels.overrides = {'1': R5_roll, '2': z, '3': N_altitude, '4': z}
        elif abs_ratio_error_longtitude > 0.5 or abs_ratio_error_longtitude == 0.5:
            vehicle.channels.overrides = {'1': R4_roll, '2': z, '3': N_altitude, '4': z}
        elif abs_ratio_error_longtitude > 0.3 or abs_ratio_error4_roll_longtitude == 0.3:
            vehicle.channels.overrides = {'1': R3_roll, '2': z, '3': N_altitude, '4': z}
        elif abs_ratio_error_longtitude > 0.15 or abs_ratio_error_longtitude == 0.15:
            vehicle.channels.overrides = {'1': R2_roll, '2': z, '3': N_altitude, '4': z}
        else:
            vehicle.channels.overrides = {'1': R1_roll, '2': z, '3': N_altitude, '4': z}

    print error_longtitude
    array_roll = np.append(array_roll, error_longtitude)

# print vehicle.channels.overrides
# np.savetxt('aalt2.txt', aalt)
x = np.arange(200000)

pl.figure(1)
line1 = pl.plot(x, array_roll)
# pl.figure(2)
# line2 = pl.plot(x, array_yaw)

# pl.savefig = ('aalt.png')
# pl.savefig = ('ayaw.png')
pl.show()

vehicle.close()
