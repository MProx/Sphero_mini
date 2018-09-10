from bluepy.btle import *
from bluepy import btle
from sphero_constants import *
import binascii
import time

'''
To do:
- Subscribe to sensor data (gyro, accelerometers, collision, landing)
'''

class sphero_mini():
    def __init__(self, MACAddr, showAcks = True):
        '''
        initialize class instance and then build collect BLE sevices and characteristics.
        Also sends text string to Anti-DOS characteristic to prevent returning to sleep,
        and initializes notifications (which is what the sphero uses to send data back to
        the client).
        '''
        self.sequence = 0
        self.showAcks = showAcks

        print("Connecting to", MACAddr)
        self.p = Peripheral(MACAddr, "random") #connect

        print("Initializing... ")

        # Subscribe to notifications
        self.sphero_delegate = MyDelegate()
        self.p.setDelegate(self.sphero_delegate)

        print(" - Read all characteristics and descriptors")
        # Get characteristics and descriptors
        self.API_V2_characteristic = self.p.getCharacteristics(uuid="00010002-574f-4f20-5370-6865726f2121")[0]
        self.AntiDOS_characteristic = self.p.getCharacteristics(uuid="00020005-574f-4f20-5370-6865726f2121")[0]
        self.DFU_characteristic = self.p.getCharacteristics(uuid="00020002-574f-4f20-5370-6865726f2121")[0]
        self.DFU2_characteristic = self.p.getCharacteristics(uuid="00020004-574f-4f20-5370-6865726f2121")[0]
        self.API_descriptor = self.API_V2_characteristic.getDescriptors(forUUID=0x2902)[0]
        self.DFU_descriptor = self.DFU_characteristic.getDescriptors(forUUID=0x2902)[0]

        # The rest of this sequence was observed during bluetooth sniffing:
        # Unlock code: prevent the sphero mini from going to sleep again after 10 seconds
        print(" - Writing AntiDOS characteristic unlock code")
        self.AntiDOS_characteristic.write("usetheforce...band".encode(), withResponse=True)

        # Enable DFU notifications:
        print(" - Configuring DFU descriptor")
        self.DFU_descriptor.write(struct.pack('<bb', 0x01, 0x00), withResponse = True)

        # No idea what this is for. Possibly a device ID of sorts? Read request returns '00 00 09 00 0c 00 02 02':
        print(" - Reading DFU2 characteristic")
        _ = self.DFU2_characteristic.read()

        # Enable API notifications:
        print(" - Configuring API dectriptor")
        self.API_descriptor.write(struct.pack('<bb', 0x01, 0x00), withResponse = True)

        self.wake()

        # Finished initializing:
        print("Initialization complete\n")

    def disconnect(self):
        print("Disconnecting")
        self.p.disconnect()

    def wake(self):
        '''
        Bring device out of sleep mode (can only be done if device was in sleep, not deep sleep).
        If in deep sleep, the device should be connected to USB power to wake.
        '''
        print(" - Waking...")
        self._send(characteristic=self.API_V2_characteristic,
                   devID=deviceID['powerInfo'],
                   commID=powerCommandIDs["wake"],
                   payload=[]) # empty payload

        self.getAcknowledgement("Wake")

    def sleep(self, deepSleep=False):
        '''
        Put device to sleep or deep sleep (deep sleep needs USB power connected to wake up)
        '''
        if deepSleep:
            sleepCommID=powerCommandIDs["deepSleep"]
            print("Going into deep sleep. Connect power to wake.")
        else:
            sleepCommID=powerCommandIDs["sleep"]
        self._send(characteristic=self.API_V2_characteristic,
                   devID=deviceID['powerInfo'],
                   commID=sleepCommID,
                   payload=[]) #empty payload

    def setLEDColor(self, red = None, green = None, blue = None):
        '''
        Set device LED color based on RGB vales (each can  range between 0 and 0xFF)
        '''
        print("Setting main LED colour to [{}, {}, {}]".format(red, green, blue))
        self._send(characteristic = self.API_V2_characteristic,
                  devID = deviceID['userIO'],
                  commID = userIOCommandIDs["allLEDs"],
                  payload = [0x00, 0x0e, red, green, blue])

        self.getAcknowledgement("LED/backlight")

    def setBackLEDIntensity(self, brightness=None):
        '''
        Set device LED backlight intensity based on 0-255 values

        NOTE: this is not the same as aiming - it only turns on the LED
        '''
        print("Setting backlight intensity to {}".format(brightness))

        self._send(characteristic = self.API_V2_characteristic,
                  devID = deviceID['userIO'],
                  commID = userIOCommandIDs["allLEDs"],
                  payload = [0x00, 0x01, brightness])

        self.getAcknowledgement("LED/backlight")

    def roll(self, speed=None, heading=None):
        '''
        Start to move the Sphero at a given direction and speed.
        heading: integer from 0 - 360 (degrees)
        speed: Integer from 0 - 255

        Note: the zero heading should be set at startup with the resetHeading method. Otherwise, it may
        seem that the sphero doesn't honor the heading argument
        '''
        print("Rolling with speed {} and heading {}".format(speed, heading))
        if abs(speed) > 255:
            print("WARNING: roll speed parameter outside of allowed range (-255 to +255)")

        if speed < 0:
            speed = -1*speed+256 # speed values > 256 in the send packet make the spero go in reverse

        speedH = (speed & 0xFF00) >> 8
        speedL = speed & 0xFF
        headingH = (heading & 0xFF00) >> 8
        headingL = heading & 0xFF
        self._send(characteristic = self.API_V2_characteristic,
                  devID = deviceID['driving'],
                  commID = drivingCommands["driveWithHeading"],
                  payload = [speedL, headingH, headingL, speedH])

        self.getAcknowledgement("Roll")

    def resetHeading(self):
        '''
        Reset the heading zero angle to the current heading (useful during aiming)
        Note: in order to manually rotate the sphero, you need to call stabilization(False).
        Once the heading has been set, call stabilization(True).
        '''
        print("Resetting heading")
        self._send(characteristic = self.API_V2_characteristic,
                  devID = deviceID['driving'],
                  commID = drivingCommands["resetHeading"],
                  payload = []) #empty payload

        self.getAcknowledgement("Heading")

    def returnMainApplicationVersion(self):
        '''
        Sends command to return application data in a notification
        '''
        print("Requesting firmware version...")
        self._send(self.API_V2_characteristic,
                   devID = deviceID['systemInfo'],
                   commID = SystemInfoCommands['mainApplicationVersion'],
                   payload = []) # empty

        self.getAcknowledgement("Firmware")

    def getBatteryVoltage(self):
        '''
        Sends command to return battery voltage data in a notification.
        Data printed to console screen by the handleNotifications() method in the MyDelegate class.
        '''
        print("Requesting battery voltage...", )
        self._send(self.API_V2_characteristic,
                   devID=deviceID['powerInfo'],
                   commID=powerCommandIDs['batteryVoltage'],
                   payload=[]) # empty

        self.getAcknowledgement("Battery")

    def stabilization(self, stab = True):
        '''
        Sends command to turn on/off the motor stabilization system (required when manually turning/aiming the sphero)
        '''
        if stab == True:
            print("Enabling stabilization... ")
            val = 1
        else:
            print("Disabling stabilization... ")
            val = 0
        self._send(self.API_V2_characteristic,
                   devID=deviceID['driving'],
                   commID=drivingCommands['stabilization'],
                   payload=[val])

        self.getAcknowledgement("Stabilization")

# =======================================================================
# The following functions are experimental:
# =======================================================================

    def configureCollisionDetection(self,
                                     xThreshold = 50, 
                                     yThreshold = 50, 
                                     xSpeed = 50, 
                                     ySpeed = 50, 
                                     deadTime = 50, # in 10 millisecond increments.
                                     method = 0x01): # Must be 0x01
        '''
        Appears to function the same as other Sphero models, however speed settings seem to have no effect. 
        From Sphero docs:
        
        xThreshold/yThreshold: An 8-bit settable threshold for the X (left/right) and Y (front/back) axes 
        of Sphero. A value of 00h disables the contribution of that axis.

        xSpeed/ySpeed: An 8-bit settable speed value for the X and Y axes. This setting is ranged by the 
        speed, then added to xThreshold, yThreshold to generate the final threshold value.
        '''
        
        print("Configuring collision detection")
        self._send(self.API_V2_characteristic,
                   devID=deviceID['sensor'],
                   commID=sensorCommands['configureCollision'],
                   payload=[method, xThreshold, xSpeed, yThreshold, ySpeed, deadTime])

        self.getAcknowledgement("Collision")

    def configureSensorStream(self): # Use default values
        '''
        Send command to configure sensor stream using default values as found during bluetooth 
        sniffing of the Sphero Edu app:
        '''
        print("Configuring sensor stream detection")
        self._send(self.API_V2_characteristic,
                   devID=deviceID['sensor'],
                   commID=sensorCommands['configureSensorStream'],
                   payload=[0x03, 0x80, 0x00, 0x00])

        self.getAcknowledgement("Sensor")

    def configureSensorMask(self): # Use default values
        '''
        Send command to configure sensor mask using default values as found during bluetooth 
        sniffing of the Sphero Edu app:
        '''
        print("Configuring sensor mask")
        self._send(self.API_V2_characteristic,
                   devID=deviceID['sensor'],
                   commID=sensorCommands['sensorMask'],
                   payload=[0x00, 0x32, 0x00, 0x00, 0x07, 0xe0, 0x78])

        self.getAcknowledgement("Mask")

# =======================================================================


    def wait(self, delay):
        '''
        This is a non-blocking delay command. It is similar to time.sleep(), except it allows asynchronous 
        notification handling to still be performed.
        '''

        start = time.time()
        while(1):
            self.p.waitForNotifications(0.001)
            if time.time() - start > delay:
                break

    def _send(self, characteristic=None, devID=None, commID=None, payload=[]):
        '''
        A generic "send" method, which will be used by other methods to send a command ID, payload and
        appropriate checksum to a specified device ID. Mainly useful because payloads are optional,
        and can be of varying length, to convert packets to binary, and calculate and send the
        checksum. For internal use only.

        Packet structure has the following format (in order):

        - Start byte: always 0x8D
        - Flags byte: indicate response required, etc
        - Virtual device ID: see sphero_constants.py
        - Command ID: see sphero_constants.py
        - Sequence number: Seems to be arbitrary. I suspect it is used to match commands to response packets (in which the number is echoed).
        - Payload: Could be varying number of bytes (incl. none), depending on the command
        - Checksum: See below for calculation
        - End byte: always 0xD8

        '''
        sendBytes = [sendPacketConstants["StartOfPacket"],
                    sum([flags["resetsInactivityTimeout"], flags["requestsResponse"]]),
                    devID,
                    commID,
                    self.sequence] + payload # concatenate payload list

        # Compute and append checksum and EOP byte:
        # From Sphero docs: "The [checksum is the] modulo 256 sum of all the bytes
        #                   from the device ID through the end of the data payload,
        #                   bit inverted (1's complement)"
        checksum = 0
        for num in sendBytes[1:]:
            checksum = (checksum + num) & 0xFF # bitwise "and to get modulo 256 sum of appropriate bytes
        checksum = 0xff - checksum # bitwise 'not' to invert checksum bits
        sendBytes += [checksum, sendPacketConstants["EndOfPacket"]] # concatenate

        # Convert numbers to bytes
        output = b"".join([x.to_bytes(1, byteorder='big') for x in sendBytes])

        #send to specified characteristic:
        characteristic.write(output, withResponse = True)

        self.sequence += 1 # Increment sequence number (not sure that this is necessary, but probably good practice)
        if self.sequence > 255:
            self.sequence = 0

    def getAcknowledgement(self, ack):
        #wait for correct acknowledgement to come in
        while(1):
            self.p.waitForNotifications(1)
            if self.sphero_delegate.notification_ack.split()[0] == ack:
                if self.showAcks:
                    print("\t" + self.sphero_delegate.notification_ack)
                else:
                    print("Unexpected ACK: {}".format(ack))
                break

class MyDelegate(btle.DefaultDelegate):

    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        self.notification_ack = "DEFAULT ACK"
        self.notificationPacket = []

    def handleNotification(self, cHandle, data):
        '''
        This method acts as an interrupt service routine. When a notification comes in, this
        method is invoked, with the variable 'cHandle' being the handle of the characteristic that
        sent the notification, and 'data' being the payload (sent one byte at a time, so the packet
        needs to be reconstructed)  

        The method keeps appending bytes to the payload packet byte list until end-of-packet byte is
        encountered. Note that this is an issue, because 0xD8 could be sent as part of the payload of,
        say, the battery voltage notification. In future, a more sophisticated method will be required.
        '''
        self.notificationPacket.append(int.from_bytes(data, byteorder="big"))
        # If end of packet:
        if data == b'\xd8' or self.notificationPacket[-1] > 256:
            # Once the packet is assembled, parse it:
            # Packet structure is similar to the outgoing send packets (see docstring in sphero_mini._send())
            # Check that first packet is start, and that the last bit is an end bit:
            if self.notificationPacket[0] != sendPacketConstants['StartOfPacket']:
                print("Unrecognized start of packet:", self.notificationPacket[0])
            elif data[-1] != sendPacketConstants['EndOfPacket']:
                print("Unrecognized end of packet:", data[-1])

            else: # Decompose packet into components:
                start, flags_bits, devid, commcode, *remainder = self.notificationPacket
                # Check if response packet:
                if flags_bits & flags['isResponse']: # it is a response
                    
                    #parse the rest of the packet
                    seq, *notification_payload, chs, end = remainder

                    # Use device ID and command code to determine which command is being acknowledged:

                    if devid == deviceID['powerInfo'] and commcode == powerCommandIDs['wake']:
                        self.notification_ack = "Wake acknowledged" # Acknowledgement after wake command
                        
                    elif devid == deviceID['powerInfo'] and commcode == powerCommandIDs['batteryVoltage']:
                        V_batt = notification_payload[2] + notification_payload[1]*256 + notification_payload[0]*65536
                        V_batt /= 100 # Notification gives V_batt in 10mV increments. Divide by 100 to get to volts.
                        self.notification_ack = "Battery voltage:" + str(V_batt) + "v"

                    elif devid == deviceID['driving'] and commcode == drivingCommands['driveWithHeading']:
                        self.notification_ack = "Roll command acknowledged"

                    elif devid == deviceID['driving'] and commcode == drivingCommands['stabilization']:
                        self.notification_ack = "Stabilization command acknowledged"

                    elif devid == deviceID['userIO'] and commcode == userIOCommandIDs['allLEDs']:
                        self.notification_ack = "LED/backlight color command acknowledged"

                    elif devid == deviceID['driving'] and commcode == drivingCommands["resetHeading"]:
                        self.notification_ack = "Heading reset command acknowledged"

                    elif devid == deviceID['sensor'] and commcode == sensorCommands["configureCollision"]:
                        self.notification_ack = "Collision detection configuration acknowledged"

                    elif devid == deviceID['sensor'] and commcode == sensorCommands["configureSensorStream"]:
                        self.notification_ack = "Sensor stream configuration acknowledged"

                    elif devid == deviceID['sensor'] and commcode == sensorCommands["sensorMask"]:
                        self.notification_ack = "Mask configuration acknowledged"

                    elif devid == deviceID['sensor'] and commcode == sensorCommands["sensor1"]:
                        self.notification_ack = "Sensor1 acknowledged"

                    elif devid == deviceID['sensor'] and commcode == sensorCommands["sensor2"]:
                        self.notification_ack = "Sensor2 acknowledged"

                    elif devid == deviceID['systemInfo'] and commcode == SystemInfoCommands['mainApplicationVersion']:
                        version = str(notification_payload[0])
                        for byte in notification_payload[1:]:
                            version += "." + str(byte)
                        self.notification_ack = "Firmware version: " + version
                                                
                    else:
                        self.notification_ack = "Unknown acknowledgement" #print(self.notificationPacket)
                        print(self.notificationPacket, "===================> Unknown packet")

                else: # Not a response packet - therefore, asynchronous notification (e.g. collision detection, etc):
                    
                    #parse the rest of the packet
                    notification_payload = remainder

                    if devid == deviceID['sensor'] and commcode == sensorCommands['collisionDetectedAsync']:
                        print("Collision detected:")
                        print(notification_payload[0], "<- always 255")
                        print(notification_payload[1])
                        print(notification_payload[2])
                        print(notification_payload[3])
                        print(notification_payload[4])
                        print(notification_payload[5], "<- always 0")
                        print(notification_payload[6], "<- always 0")
                        print(notification_payload[7], "<- Axis")
                        print(notification_payload[8], "<- always 0")
                        print(notification_payload[9], "<- X Magnitude")
                        print(notification_payload[10], "<- always 0")
                        print(notification_payload[11], "<- Y Magnitude" )
                        print(notification_payload[12], "<- Time stamp")
                    # TODO: parse other types of asynch notifications (sensors data, battery voltage, etc)

                    else:
                        self.notification_ack = "Unknown asynchronous notification" #print(self.notificationPacket)
                        print(self.notificationPacket, "===================> Unknown packet")
                        

                    
            self.lastPacket = self.notificationPacket
            self.notificationPacket = [] # Start new payload after this byte
