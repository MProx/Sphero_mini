import sphero_mini
import sys

if len(sys.argv) < 2:
    print("Usage: 'python [this_file_name.py] [sphero MAC address]'")
    print("eg f2:54:32:9d:68:a4")
    print("On Linux, use 'sudo hcitool lescan' to find your Sphero Mini's MAC address")
    exit(1)

MAC = sys.argv[1] # Get MAC address from command line argument

# Connect:
sphero = sphero_mini.sphero_mini(MAC, verbosity = 1)

# Sends instruction to return battery voltage
# (Printed to the console screen as a notification)
sphero.getBatteryVoltage()

# Get firmware version number
# (Printed to the console screen as a notification)
sphero.returnMainApplicationVersion()

# Aiming:
sphero.setLEDColor(red = 0, green = 0, blue = 0) # Turn main LED off
sphero.stabilization(False) # Turn off stabilization
sphero.setBackLEDIntensity(255) # turn back LED on
sphero.wait(3) # Non-blocking pau`se
sphero.resetHeading() # Reset heading
sphero.stabilization(True) # Turn on stabilization
sphero.setBackLEDIntensity(0) # Turn back LED off

# Move around:
sphero.setLEDColor(red = 0, green = 0, blue = 255) # Turn main LED blue
sphero.roll(50, 0)      # roll forwards (heading = 0) at speed = 50

sphero.wait(3)         # Keep rolling for three seconds

sphero.roll(0, 0)       # stop
sphero.wait(1)          # Allow time to stop

sphero.setLEDColor(red = 0, green = 255, blue = 0) # Turn main LED green
sphero.roll(-50, 0)     # Keep facing forwards but roll backwards at speed = 50
sphero.wait(3)          # Keep rolling for three seconds

sphero.roll(0, 0)       # stop
sphero.wait(1)          # Allow time to stop

sphero.sleep()
sphero.disconnect()
