# Sphero_mini
An unofficial Python library (work in progress) for controlling the [Sphero Mini](https://www.sphero.com/sphero-mini) robot. Note that, because the communications protocols are very different, this library is unlikely to work out-of-the-box for other types of Sphero robots (e.g. BB8, BB9, SPRK+, etc)

## Progress:
I am actively working on this project, but it is still in it's infancy. For now, this library can only do the following:
* Come out of sleep mode
* Reset the heading (aiming)
* Query the battery voltage
* Change the LED's colour
* Set back LED intensity
* Roll in a specified direction at a given speed
* Go back to sleep (or deep sleep)

### To do:
* Find out how to receive sensor data (accelerometer, gyro, collision detection, etc) - requires sending write request to the correct characteristic, and then parsing the resulting stream of notifications.

## Dependencies:
This library is being tested with Python 3.2.5, but should work for other 3.x versions. This library also uses the Bluepy module for BLE communication, so make sure this is installed. On Debian-based Linux:

    $ sudo apt-get install python-pip libglib2.0-dev
    $ pip install bluepy --user
## Known issues and work-arounds:
* Sometimes, the bluetooth module fails to connect. If this happens, try again. If it keeps failing, double-check your MAC address.
* If it keeps failing after that, try re-booting your computer. I find that, expecially after terminating a script with a keyboard interrupt (ctrl+C), the bluetooth module may struggle to reconnect afterwards
* The notifications (messages returned from the sphero to the client) are a little experimental right now. Messages may not come through, or may not come through immediately. Do not rely on things like command acknowledgements, battery voltage reporting, etc.

## Usage:
The class methods are well commented, so for usage of each, see sphero_mini.py. 

Save the below script to a .py file, and make sure that sphero_mini.py is saved in the same folder, then run the following command from linux command prompt:

    $ python [this_file_name.py] [sphero MAC address]

For example:

    $ python sphero_example.py f2:54:32:9d:68:a4

Here's a basic script that illustrates currently available functions. 

    import sphero_mini
    import time
    import sys

    if len(sys.argv) < 2:
        print("Usage: 'python [this_file_name.py] [sphero MAC address]'")
        print("eg f2:54:32:9d:68:a4")
        print("On Linux, use 'sudo hcitool lescan' to find your Sphero Mini's MAC address")
        exit(1)

    MAC = sys.argv[1] # Get MAC address from command line argument

    # Connect:
    sphero = sphero_mini.sphero_mini(MAC)

    # Sends instruction to return battery voltage
    # (Printed to the console screen as a notification)
    sphero.getBatteryVoltage()

    # Aiming:
    sphero.setLEDColor(red = 0, green = 0, blue = 0) # Turn main LED off
    sphero.setBackLEDIntensity(255) # turn back LED on
    time.sleep(3) # Wait 3 seconds while user aims device
    sphero.resetHeading() # Reset heading
    sphero.setBackLEDIntensity(0) # Turn back LED off

    # Roll forward for 1 second
    sphero.setLEDColor(red = 0, green = 0, blue = 255) # Turn main LED blue
    sphero.roll(50, 0)  # roll forwards (heading = 0) at speed = 50
    time.sleep(3)       # keep rolling for 1 second
    sphero.roll(0, 0)   # stop
    time.sleep(1)       # Wait to come to a stop
    sphero.setLEDColor(red = 0, green = 255, blue = 0) # Turn main LED green
    sphero.roll(-50, 0) # roll backwards at speed = 50 for 1 second
    time.sleep(3)       # Keep rolling for 1 second
    sphero.roll(0, 0)   # stop
    time.sleep(1)       # Wait to come to a stop

    sphero.sleep()
    sphero.disconnect()
