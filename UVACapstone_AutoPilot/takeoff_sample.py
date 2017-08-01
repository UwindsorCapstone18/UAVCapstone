
from dronekit import connect, VehicleMode, LocationGlobalRelative
import dronekit
import time
import numpy as np
from matplotlib import pylab as pl
from getkey import getkey, keys

vehicle = dronekit.connect('tcp:127.0.0.1:5760', baud=57600, heartbeat_timeout=20)
aalt = []
def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)

    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print "Reached target altitude"
            break
        time.sleep(1)


arm_and_takeoff(50)

for i in range(0,100):
    altitude = vehicle.location.global_relative_frame.alt
    print vehicle.location.global_relative_frame.alt
    time.sleep()
    aalt = np.append(aalt, altitude)

np.savetxt('simpletakeoff.txt', aalt)
y = np.arange(100)

line1 = pl.plot(y, aalt)
pl.setp(line1, label='avd', color='b')
pl.savefig = ('simpletakeoff.png')
pl.show()

vehicle.close()
