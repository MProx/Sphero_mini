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

# battery voltage
sphero.getBatteryVoltage()
print(f"Bettery voltage: {sphero.v_batt}v")

# firmware version number
sphero.returnMainApplicationVersion()
print(f"Firmware version: {'.'.join(str(x) for x in sphero.firmware_version)}")

#Configure sensors to make IMU_yaw values available
sphero.configureSensorMask(IMU_yaw=True)
sphero.configureSensorStream()

print("Rotate device through 360 degrees on vertical axis to change colours")
while(1):
    yaw = sphero.IMU_yaw
    print("Yaw angle: {}".format(round(yaw, 3)))
    if yaw > 0:
        sphero.setLEDColor(red = 0, green = 255, blue = 0) # Turn LEDs green
    else:
        sphero.setLEDColor(red = 0, green = 0, blue = 255) # Turn LEDs green