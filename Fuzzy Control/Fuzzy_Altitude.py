import dronekit as dk
import time
import math
import numpy as np
import decimal
from matplotlib import pylab as pl
from getkey import getkey, keys

vehicle = dk.connect('tcp:127.0.0.1:5760', baud=57600, heartbeat_timeout=20)

# Basic Parameters
z1 = 1499
z2 = 1517
z3 = 1220
z4 = 1506
array_altitude = []
vehicle.channels.overrides = {'1': z, '2': z, '3': 992, '4': z}

# Altitude Input
set_altitude = 1

# Armed and Takeoff
print "Arming motors"
vehicle.mode = dk.VehicleMode("STABILIZE")
print vehicle.mode
vehicle.armed = True
time.sleep(2)
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
    # ratio_error_altitude = float(error_altitude) / float(set_altitude)
    # abs_ratio_error_altitude = abs(ratio_error_altitude)
    # Altitude Gears
    N_altitude = 1361
    R_altitude = N_altitude - math.exp(abs(error_altitude))
    D_altitude = N_altitude + math.exp(abs(error_altitude))

    if error_altitude > 0:
        vehicle.channels.overrides = {'1': z1, '2': z2, '3': D_altitude, '4': z4}
    else:
        vehicle.channels.overrides = {'1': z1, '2': z2, '3': R_altitude, '4': z4}
    print altitude
    array_altitude = np.append(array_altitude, altitude)

    # altitude = vehicle.location.global_relative_frame.alt
    # error_altitude = set_altitude - altitude
    # ratio_error_altitude = float(error_altitude) / float(set_altitude)
    # abs_ratio_error_altitude = abs(ratio_error_altitude)
    #
    # if abs_ratio_error_altitude < 0.05 or abs_ratio_error_altitude == 0.05:
    #     vehicle.channels.overrides = {'1': z1, '2': z2, '3': N_altitude, '4': z4}
    # elif ratio_error_altitude > 0.05:
    #     if abs_ratio_error_altitude > 0.7 or abs_ratio_error_altitude == 0.7:
    #         vehicle.channels.overrides = {'1': z1, '2': z2, '3': D5_altitude, '4': z4}
    #     elif abs_ratio_error_altitude > 0.5 or abs_ratio_error_altitude == 0.5:
    #         vehicle.channels.overrides = {'1': z1, '2': z2, '3': D4_altitude, '4': z4}
    #     elif abs_ratio_error_altitude > 0.3 or abs_ratio_error_altitude == 0.3:
    #         vehicle.channels.overrides = {'1': z1, '2': z2, '3': D3_altitude, '4': z4}
    #     elif abs_ratio_error_altitude > 0.15 or abs_ratio_error_altitude == 0.15:
    #         vehicle.channels.overrides = {'1': z1, '2': z2, '3': D2_altitude, '4': z4}
    #     else:
    #         vehicle.channels.overrides = {'1': z1, '2': z2, '3': D1_altitude, '4': z4}
    # else:
    #     if abs_ratio_error_altitude > 0.7 or abs_ratio_error_altitude == 0.7:
    #         vehicle.channels.overrides = {'1': z1, '2': z2, '3': R5_altitude, '4': z4}
    #     elif abs_ratio_error_altitude > 0.5 or abs_ratio_error_altitude == 0.5:
    #         vehicle.channels.overrides = {'1': z1, '2': z2, '3': R4_altitude, '4': z4}
    #     elif abs_ratio_error_altitude > 0.3 or abs_ratio_error_altitude == 0.3:
    #         vehicle.channels.overrides = {'1': z1, '2': z2, '3': R3_altitude, '4': z4}
    #     elif abs_ratio_error_altitude > 0.15 or abs_ratio_error_altitude == 0.15:
    #         vehicle.channels.overrides = {'1': z1, '2': z2, '3': R2_altitude, '4': z4}
    #     else:
    #         vehicle.channels.overrides = {'1': z1, '2': z2, '3': R1_altitude, '4': z4}
    #
    # print altitude
    # array_altitude = np.append(array_altitude, altitude)

# print vehicle.channels.overrides
# np.savetxt('aalt2.txt', aalt)
x = np.arange(200000)

pl.figure(1)
line1 = pl.plot(x, array_altitude)
# pl.figure(2)
# line2 = pl.plot(x, array_yaw)

# pl.savefig = ('aalt.png')
# pl.savefig = ('ayaw.png')
pl.show()

vehicle.close()
