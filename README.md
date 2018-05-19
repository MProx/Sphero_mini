# Sphero_mini
An unofficial Python library (work in progress) for controlling the sphero mini robot

## Dependencies:
Uses the Bluepy library for BLE communication, so make sure this is installed:

    pip install bluepy --user
    
## Progress:
I am actively working on this project, but it is in it's infancy. For now, this library can only make the Sphero Mini come out of sleep, change the LED's colour, and then go back to sleep (or deep sleep).

## Usage:
    import sphero_mini
    import time
    import random

    sphero = sphero_mini.sphero_mini("f2:54:32:9d:68:a4")

    sphero.wake()

    sphero.setLEDColour(red=30, green=30, blue=30)
    sphero.setBackLEDIntensity(250)
    time.sleep(2)
    sphero.setBackLEDIntensity(0)

    for i in range(3):
        sphero.setLEDColour(red=0xff, green=0, blue=0)
        time.sleep(0.5)
        sphero.setLEDColour(red=0, green=0xff, blue=0)
        time.sleep(0.5)
        sphero.setLEDColour(red=0, green=0, blue=0xff)
        time.sleep(0.5)

    # sphero.roll(speed = 50, heading= 180)
    time.sleep(2) # keep rolling for 2 second
    sphero.roll(speed = 0, heading = 0) #stop
    time.sleep(2) # allow time to stabilize before sleeping

    sphero.sleep()

    sphero.disconnect()
