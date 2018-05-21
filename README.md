# Sphero_mini
An unofficial Python library (work in progress) for controlling the [Sphero Mini](https://www.sphero.com/sphero-mini) robot

## Progress:
I am actively working on this project, but it is still in it's infancy. For now, this library can only do the following:
* Come out of sleep mode
* Reset the heading (aiming)
* Change the LED's colour
* Set back LED intensity
* Roll in a specified direction at a given speed
* Go back to sleep (or deep sleep)

### To do:
* Subscribe to notifications from BLE characteristics, and receive sensor data (accelerometer, gyro, collision detection, etc)

## Dependencies:
This library is being tested with Python 3.2.5, but should work for other 3.x versions. This library also uses the Bluepy module for BLE communication, so make sure this is installed. On Linux:

    pip install bluepy --user
    
## Usage:
The class methods are well commented, so for usage of each, see sphero_mini.py. 

Here's a basic script that illustrates currently available functions:

    import sphero_mini
    import time

    # Replace with your own Sphero Mini's MAC address (on Linux, use "sudo hcitool lescan")
    MAC = "f2:54:32:9d:68:a4"
    sphero = sphero_mini.sphero_mini(MAC)

    sphero.wake()

    # Aiming:
    sphero.setLEDColour(red = 0, green = 0, blue = 0)   # Turn main LED off
    sphero.setBackLEDIntensity(255)                     # Turn back LED on
    time.sleep(3)                                       # Wait 3 seconds while user aims device
    sphero.resetHeading()                               # Reset heading
    sphero.setBackLEDIntensity(0)                       # Turn back LED off

    # Turn main LED green:
    sphero.setLEDColour(red = 0,
                     green = 255,
                     blue = 0)

    # roll in specified direction at 80 speed  for 2 seconds
    sphero.roll(80, 0)
    time.sleep(2)
    sphero.roll(0, 180)

    time.sleep(1) # Allow device to come to a stop

    # Come back to start position
    sphero.roll(80, 180)
    time.sleep(2)
    sphero.roll(0, 0)
    sphero.setLEDColour(red = 0, green = 0, blue = 0)   # Turn main LED off

    time.sleep(1) # Allow device to come to a stop

    sphero.sleep()

    sphero.disconnect()
