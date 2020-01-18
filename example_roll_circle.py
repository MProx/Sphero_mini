import sphero_mini
import sys
import time

if len(sys.argv) < 2:
    print("Usage: 'python [this_file_name.py] [sphero MAC address]'")
    print("eg f2:54:32:9d:68:a4")
    print("On Linux, use 'sudo hcitool lescan' to find your Sphero Mini's MAC address")
    raise SystemExit

MAC = sys.argv[1] # Get MAC address from command line argument

# Connect:
sphero = sphero_mini.sphero_mini(MAC, verbosity = 4)

# battery voltage
sphero.getBatteryVoltage()
print("Battery voltage: " + str(sphero.v_batt) + " V")

# firmware version number
sphero.returnMainApplicationVersion()
print("Firmware version: " + '.'.join(str(x) for x in sphero.firmware_version))

# Aiming:
sphero.setLEDColor(red = 0, green = 0, blue = 0) # Turn main LED off
sphero.stabilization(False) # Turn off stabilization
sphero.setBackLEDIntensity(255) # turn back LED on
sphero.wait(3) # Non-blocking pau`se
sphero.resetHeading() # Reset heading
sphero.stabilization(True) # Turn on stabilization
sphero.setBackLEDIntensity(0) # Turn back LED off

# Move around:
angle = 0
angle_increment = 25
start = time.time()

# Approximate a circle by moving forward in short bursts, then adjusting heading slightly
while(time.time() - start < 30):
    
    sphero.setLEDColor(red = 0, green = 0, blue = 255) # Turn main LED blue
    sphero.roll(30, angle)  # roll forwards (heading = 0) at speed = 50

    sphero.wait(0.5)          # Keep rolling for three seconds

    angle += angle_increment
    if angle >= 360:
        angle = 0

sphero.roll(0, 0)       # stop
sphero.wait(1)          # Allow time to stop

sphero.sleep()
sphero.disconnect()
