# Sphero Mini
An unofficial Python library (work in progress) for controlling the [Sphero Mini](https://www.sphero.com/sphero-mini) robot. Note that, because the communications protocols are very different, this library will not work out-of-the-box for other types of Sphero robots (e.g. BB8, BB9, SPRK+, etc).

If you use this library for anything fun, please let me know - MProx.contact@gmail.com

## Dependencies:
This library is being tested with Python 3.6.5, but should work for other 3.x versions. This library also uses the Bluepy module for BLE communication, so make sure this is installed. On Debian-based Linux:

    $ sudo apt-get install libglib2.0-dev
    $ pip install bluepy --user

## Usage:
The class methods are well commented, so for usage of each, see sphero_mini.py. 

As an example demonstrating basic usage, see run.py. Make sure that both sphero_mini.py and sphero_constants.py are saved in the same folder as run.py. Then from linux command prompt, navigate to that folder and run the following command:

    $ python run.py [sphero MAC address]

On Linux, use 'sudo hcitool lescan' to find your Sphero Mini's MAC address.

Note on usage: If you need to use delays, you can use time.sleep(), but this is a blocking function. Any asynchronous notifications that come in during the delay period can only be processed when it ends. If you need asynchronous commands (e.g. collision detection) to be processed immediately, use the provided convenience function:

    sphero.wait(delay)

where delay is a value in seconds.

## Troubleshooting, known issues and work-arounds:
* Sometimes, the bluetooth module fails to connect. If this happens, try again. If it keeps failing, double-check your MAC address.
* If it still fails, try connecting the sphero to USB power briefly and then disconnecting. This resets the microcontroller.
* If it keeps failing after that, try re-booting your computer. I find that, expecially after terminating a script with a keyboard interrupt (ctrl+C), the bluetooth module may struggle to reconnect afterwards
* The notifications (messages returned from the sphero to the client) are a little experimental right now. Messages may not come through, or may not come through immediately. Do not rely on things like command acknowledgements, battery voltage reporting, etc. 
* Sometimes, bluetooth collisions seem to happen, possibly caused by unexpected asynchronous notifications (e.g. collision detection) coming in at a poor time. I have not found a way to prevent them. They cause the program to crash and it needs to be restarted, but they seem to be quite rare.

## Progress:
I am actively working on this project, but it is still in it's infancy. For now, this library can only do the following:
* Come out of sleep mode
* Reset the heading (aiming)
* Query the battery voltage
* Change the LED's colour
* Set back LED intensity
* Roll in a specified direction at a given speed
* Go back to sleep (or deep sleep)
* Detect collisions and produce as-yet partially-parsed collision detection information
* Return un-parsed sensor data (from all sensors) and display it on the console screen. Example output:

> 1126040543980291845585399799275653923201955500894
> 475230771193920660464026295803746961480564251780
> 373480289031629483274603252027886583861619413251
> 350557861046320592069853442054633908532194215389
> 357721051403455528023241278566341852345862299969

## Current areas of development:
* The collision detection function works, but the reurned data is only partially parsed. Configure by calling 'sphero.configureCollisionDetection()', which sets the default thresholds. When a collision that exceeds the threshold is detected, an asynchronous bluetooth notification is received and the results will be displayed on the console with the suspected values of what the numbers represent. Note that the X/Y axis threshold values seem to work, but the speed scaling values seem to have no effect.

* The sensor stream can be configured to output unparsed sensor data to the console. The sensor stream is configured by calling 'sphero.configureSensorMask()' followed by 'sphero.configureSensorStream()'. These apply the default values as observed in bluetooth packet sniffing, however it is unclear what they actually mean. After calling these functions, a large amount of data will be received in a continuous stream, and will be displayed to the console screen.
