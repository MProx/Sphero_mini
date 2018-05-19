# Sphero_mini
An unofficial library (work in progress) for controlling the sphero mini robot

## Dependencies:
Uses the Bluepy library for BLE communication, so make sure this is installed:

    pip install bluepy --user
    
## Progress:
I am actively working on this project, but it is in it's infancy. For now, this library can only make the Sphero Mini come out of sleep, change the LED's colour, and then go back to sleep (or deep sleep).

## Usage:
    import sphero_mini
    import time
    import random

    sphero = sphero_mini.sphero_mini("f2:54:32:9d:68:a4") #Insert your own sphero mini's MAC address here

    sphero.wake()

    for i in range(5):
        sphero.setLEDColour(red = random.randint(0, 255),
                             green = random.randint(0, 255),
                             blue = random.randint(0, 255))
        time.sleep(0.5)

    sphero.sleep()

    sphero.p.disconnect()
