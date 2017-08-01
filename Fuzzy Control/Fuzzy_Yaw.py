import dronekit as dk
import time
import math
import numpy as np
import decimal
from matplotlib import pylab as pl
from getkey import getkey, keys

vehicle = dk.connect('tcp:127.0.0.1:5760', baud=57600, heartbeat_timeout=20)

# Basic Parameters
z = 1472
array_yaw = []
vehicle.channels.overrides = {'1': z, '2': z, '3': 992, '4': z}

# Angle Input
set_angle = 0

# Yaw Gears
N_yaw = 1508  # 1472-1535 is the range for N gear

R1_yaw = N_yaw - math.exp(3.6)      #Min=3.6
R2_yaw = R1_yaw - math.exp(3.62)
R3_yaw = R1_yaw - math.exp(3.65)
R4_yaw = R1_yaw - math.exp(3.68)
R5_yaw = R1_yaw - math.exp(3.70)

D1_yaw = N_yaw + math.exp(3.3)     #Min=3.3
D2_yaw = D1_yaw + math.exp(3.32)
D3_yaw = D1_yaw + math.exp(3.35)
D4_yaw = D1_yaw + math.exp(3.38)
D5_yaw = D1_yaw + math.exp(3.40)

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

# Rotation
for k in range(0, 200000):
    yaw = vehicle.attitude.yaw
    angle = round((yaw / np.pi) * 180, 2)
    error_angle = set_angle - angle
    abs_error_angle = abs(error_angle)

    if abs_error_angle < 1 or abs_error_angle == 1:
        vehicle.channels.overrides = {'1': z, '2': z, '3': N_altitude, '4': N_yaw}
    elif error_angle > 1:
        if abs_error_angle > 20 or abs_error_angle == 20:
            vehicle.channels.overrides = {'1': z, '2': z, '3': N_altitude, '4': D5_yaw}
        elif abs_error_angle > 10 or abs_error_angle == 10:
            vehicle.channels.overrides = {'1': z, '2': z, '3': N_altitude, '4': D4_yaw}
        elif abs_error_angle > 5 or abs_error_angle == 5:
            vehicle.channels.overrides = {'1': z, '2': z, '3': N_altitude, '4': D3_yaw}
        elif abs_error_angle > 3 or abs_error_angle == 3:
            vehicle.channels.overrides = {'1': z, '2': z, '3': N_altitude, '4': D2_yaw}
        else:
            vehicle.channels.overrides = {'1': z, '2': z, '3': N_altitude, '4': D1_yaw}
    else:
        if abs_error_angle > 20 or abs_error_angle == 20:
            vehicle.channels.overrides = {'1': z, '2': z, '3': N_altitude, '4': R5_yaw}
        elif abs_error_angle > 10 or abs_error_angle == 10:
            vehicle.channels.overrides = {'1': z, '2': z, '3': N_altitude, '4': R4_yaw}
        elif abs_error_angle > 5 or abs_error_angle == 5:
            vehicle.channels.overrides = {'1': z, '2': z, '3': N_altitude, '4': R3_yaw}
        elif abs_error_angle > 3 or abs_error_angle == 3:
            vehicle.channels.overrides = {'1': z, '2': z, '3': N_altitude, '4': R2_yaw}
        else:
            vehicle.channels.overrides = {'1': z, '2': z, '3': N_altitude, '4': R1_yaw}

    print angle
    array_yaw = np.append(array_yaw, angle)

# print vehicle.channels.overrides
# np.savetxt('aalt2.txt', aalt)
x = np.arange(200000)

# pl.figure(1)
# line1 = pl.plot(x, array_altitude)
pl.figure(2)
line2 = pl.plot(x, array_yaw)
#
# # pl.savefig = ('aalt.png')
# # pl.savefig = ('ayaw.png')
pl.show()

vehicle.close()
