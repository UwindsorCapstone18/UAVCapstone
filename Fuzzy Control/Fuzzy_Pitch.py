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
array_pitch = []
vehicle.channels.overrides = {'1': z, '2': z, '3': 992, '4': z}
# Current Latitude(42.3046647,-83.0617518)

# Latitude Input
set_latitude = 566.47

# Pitch Gears
N_pitch = 1472

R1_pitch = 1550        #N_pitch + math.exp(1)
R2_pitch = 1650        #R1_pitch + math.exp(3)
R3_pitch = 1750        #R1_pitch + math.exp(4)
R4_pitch = 1850        #R1_pitch + math.exp(5)
R5_pitch = 1950        #R1_pitch + math.exp(6)

D1_pitch = 1422        #N_pitch - math.exp(1)
D2_pitch = 1372        #D1_pitch - math.exp(3)
D3_pitch = 1322        #D1_pitch - math.exp(4)
D4_pitch = 1272        #D1_pitch - math.exp(5)
D5_pitch = 1222        #D1_pitch - math.exp(6)

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

# Gain Pitch
for l in range(0, 200000):

    current_latitude = vehicle.location.global_relative_frame.lat
    current_latitude = round((current_latitude * 100 - np.fix(current_latitude * 100)) * 1000, 2)
    error_latitude = set_latitude - current_latitude
    abs_error_latitude = abs(error_latitude)
    ratio_error_latitude = float(error_latitude) / float(set_latitude)
    abs_ratio_error_latitude = abs(ratio_error_latitude)

    if abs_error_latitude < 0.5 or abs_error_latitude == 0.5:
        vehicle.channels.overrides = {'1': z, '2': N_pitch, '3': N_altitude, '4': z}
    elif abs_error_latitude > 0.5 :
        if abs_ratio_error_latitude > 0.7 or abs_ratio_error_latitude == 0.7:
            vehicle.channels.overrides = {'1': z, '2': D5_pitch, '3': N_altitude, '4': z}
        elif abs_ratio_error_latitude > 0.5 or abs_ratio_error_latitude == 0.5:
            vehicle.channels.overrides = {'1': z, '2': D4_pitch, '3': N_altitude, '4': z}
        elif abs_ratio_error_latitude > 0.3 or abs_ratio_error_latitude == 0.3:
            vehicle.channels.overrides = {'1': z, '2': D3_pitch, '3': N_altitude, '4': z}
        elif abs_ratio_error_latitude > 0.15 or abs_ratio_error_latitude == 0.15:
            vehicle.channels.overrides = {'1': z, '2': D2_pitch, '3': N_altitude, '4': z}
        else:
            vehicle.channels.overrides = {'1': z, '2': D1_pitch, '3': N_altitude, '4': z}
    else:
        if abs_ratio_error_latitude > 0.7 or abs_ratio_error_latitude == 0.7:
            vehicle.channels.overrides = {'1': z, '2': R5_pitch, '3': N_altitude, '4': z}
        elif abs_ratio_error_latitude > 0.5 or abs_ratio_error_latitude == 0.5:
            vehicle.channels.overrides = {'1': z, '2': R4_pitch, '3': N_altitude, '4': z}
        elif abs_ratio_error_latitude > 0.3 or abs_ratio_error_latitude == 0.3:
            vehicle.channels.overrides = {'1': z, '2': R3_pitch, '3': N_altitude, '4': z}
        elif abs_ratio_error_latitude > 0.15 or abs_ratio_error_latitude == 0.15:
            vehicle.channels.overrides = {'1': z, '2': R2_pitch, '3': N_altitude, '4': z}
        else:
            vehicle.channels.overrides = {'1': z, '2': R1_pitch, '3': N_altitude, '4': z}

    print error_latitude
    array_pitch = np.append(array_pitch, error_latitude)

# print vehicle.channels.overrides
# np.savetxt('aalt2.txt', aalt)
x = np.arange(200000)

pl.figure(1)
line1 = pl.plot(x, array_pitch)
# pl.figure(2)
# line2 = pl.plot(x, array_yaw)

# pl.savefig = ('aalt.png')
# pl.savefig = ('ayaw.png')
pl.show()

vehicle.close()
