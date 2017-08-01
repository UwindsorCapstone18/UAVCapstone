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
array_altitude = []
array_pitch = []
vehicle.channels.overrides = {'1': z, '2': z, '3': 992, '4': z}
# Current GPS(42.3046647,-83.0617518)

# Altitude Input
set_altitude = 1.5

# Latitude Input
set_latitude = 486.47

# Altitude Gears
N_altitude = 1361

R1_altitude = N_altitude - math.exp(0.2)
R2_altitude = R1_altitude - math.exp(0.3)
R3_altitude = R1_altitude - math.exp(0.4)
R4_altitude = R1_altitude - math.exp(0.5)
R5_altitude = R1_altitude - math.exp(0.6)

D1_altitude = N_altitude + math.exp(0.2)
D2_altitude = D1_altitude + math.exp(0.3)
D3_altitude = D1_altitude + math.exp(0.4)
D4_altitude = D1_altitude + math.exp(0.5)
D5_altitude = D1_altitude + math.exp(1.7)

# Pitch Gears
N_pitch = 1472

R1_pitch = N_pitch + math.exp(2)
R2_pitch = N_pitch + math.exp(3)
R3_pitch = N_pitch + math.exp(4)
R4_pitch = N_pitch + math.exp(5)
R5_pitch = N_pitch + math.exp(6)

D1_pitch = N_pitch - math.exp(2)
D2_pitch = N_pitch - math.exp(3)
D3_pitch = N_pitch - math.exp(4)
D4_pitch = N_pitch - math.exp(5)
D5_pitch = N_pitch - math.exp(6)

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

# Gain Altitude
for j in range(0, 100000):

    altitude = vehicle.location.global_relative_frame.alt
    error_altitude = set_altitude - altitude
    ratio_error_altitude = float(error_altitude) / float(set_altitude)
    abs_ratio_error_altitude = abs(ratio_error_altitude)

    if abs_ratio_error_altitude < 0.05 or abs_ratio_error_altitude == 0.05:
        vehicle.channels.overrides = {'1': z, '2': z, '3': N_altitude, '4': z}
    elif ratio_error_altitude > 0.05:
        if abs_ratio_error_altitude > 0.7 or abs_ratio_error_altitude == 0.7:
            vehicle.channels.overrides = {'1': z, '2': z, '3': D5_altitude, '4': z}
        elif abs_ratio_error_altitude > 0.5 or abs_ratio_error_altitude == 0.5:
            vehicle.channels.overrides = {'1': z, '2': z, '3': D4_altitude, '4': z}
        elif abs_ratio_error_altitude > 0.3 or abs_ratio_error_altitude == 0.3:
            vehicle.channels.overrides = {'1': z, '2': z, '3': D3_altitude, '4': z}
        elif abs_ratio_error_altitude > 0.15 or abs_ratio_error_altitude == 0.15:
            vehicle.channels.overrides = {'1': z, '2': z, '3': D2_altitude, '4': z}
        else:
            vehicle.channels.overrides = {'1': z, '2': z, '3': D1_altitude, '4': z}
    else:
        if abs_ratio_error_altitude > 0.7 or abs_ratio_error_altitude == 0.7:
            vehicle.channels.overrides = {'1': z, '2': z, '3': R5_altitude, '4': z}
        elif abs_ratio_error_altitude > 0.5 or abs_ratio_error_altitude == 0.5:
            vehicle.channels.overrides = {'1': z, '2': z, '3': R4_altitude, '4': z}
        elif abs_ratio_error_altitude > 0.3 or abs_ratio_error_altitude == 0.3:
            vehicle.channels.overrides = {'1': z, '2': z, '3': R3_altitude, '4': z}
        elif abs_ratio_error_altitude > 0.15 or abs_ratio_error_altitude == 0.15:
            vehicle.channels.overrides = {'1': z, '2': z, '3': R2_altitude, '4': z}
        else:
            vehicle.channels.overrides = {'1': z, '2': z, '3': R1_altitude, '4': z}

    print altitude
    array_altitude = np.append(array_altitude, altitude)

# Gain Pitch
for l in range(0, 300000):

    current_latitude = vehicle.location.global_relative_frame.lat
    current_latitude = round((current_latitude * 100 - np.fix(current_latitude * 100))* 1000, 2)
    error_latitude = (set_latitude - current_latitude)*(float(111)/float(100))
    abs_error_latitude = abs(error_latitude)
    ratio_error_latitude = float(error_latitude) / float(set_latitude)
    abs_ratio_error_latitude = abs(ratio_error_latitude)

    if abs_error_latitude < 0.5 or abs_error_latitude == 0.5:
        vehicle.channels.overrides = {'1': z, '2': N_pitch, '3': N_altitude, '4': z}
    elif error_latitude > 0.5:
        if abs_ratio_error_latitude > 0.5 or abs_ratio_error_latitude == 0.5:
            vehicle.channels.overrides = {'1': z, '2': D5_pitch, '3': N_altitude, '4': z}
        elif abs_ratio_error_latitude > 0.3 or abs_ratio_error_latitude == 0.3:
            vehicle.channels.overrides = {'1': z, '2': D4_pitch, '3': N_altitude, '4': z}
        elif abs_ratio_error_latitude > 0.15 or abs_ratio_error_latitude == 0.15:
            vehicle.channels.overrides = {'1': z, '2': D3_pitch, '3': N_altitude, '4': z}
        elif abs_ratio_error_latitude > 0.05 or abs_ratio_error_latitude == 0.05:
            vehicle.channels.overrides = {'1': z, '2': D2_pitch, '3': N_altitude, '4': z}
        else:
            vehicle.channels.overrides = {'1': z, '2': D1_pitch, '3': N_altitude, '4': z}
    else:
        if abs_ratio_error_latitude > 0.5 or abs_ratio_error_latitude == 0.5:
            vehicle.channels.overrides = {'1': z, '2': R5_pitch, '3': N_altitude, '4': z}
        elif abs_ratio_error_latitude > 0.3 or abs_ratio_error_latitude == 0.3:
            vehicle.channels.overrides = {'1': z, '2': R4_pitch, '3': N_altitude, '4': z}
        elif abs_ratio_error_latitude > 0.15 or abs_ratio_error_latitude == 0.15:
            vehicle.channels.overrides = {'1': z, '2': R3_pitch, '3': N_altitude, '4': z}
        elif abs_ratio_error_latitude > 0.05 or abs_ratio_error_latitude == 0.05:
            vehicle.channels.overrides = {'1': z, '2': R2_pitch, '3': N_altitude, '4': z}
        else:
            vehicle.channels.overrides = {'1': z, '2': R1_pitch, '3': N_altitude, '4': z}

    print vehicle.channels.overrides
    print error_latitude
    array_pitch = np.append(array_pitch, error_latitude)


# np.savetxt('aalt2.txt', aalt)
x1 = np.arange(100000)
x2 = np.arange(300000)

pl.figure(1)
line1 = pl.plot(x1, array_altitude)
pl.figure(2)
line2 = pl.plot(x2, array_pitch)

# pl.savefig = ('aalt.png')
# pl.savefig = ('ayaw.png')
pl.show()

vehicle.close()
