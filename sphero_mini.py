from bluepy.btle import *
from bluepy import btle
from sphero_constants import *
import binascii

'''
To do:
- Subscribe to sensor data (gyro, accelerometers, collision, landing)
'''

class sphero_mini():
    def __init__(self, MACAddr):
        '''
        initialize class instance and then build collect BLE sevices and characteristics.
        Also sends text string to Anti-DOS characteristic to prevent returning to sleep,
        and initializes notifications (which is what the sphero uses to send data back to
        the client).
        '''
        self.sequence = 0

        print("Connecting to", MACAddr)
        self.p = Peripheral(MACAddr, "random") #connect

        print("Initializing... ")

        # Subscribe to notifications
        self.p.setDelegate(MyDelegate())

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
        print(" - Writing 0x0001 to DFU descriptor")
        self.DFU_descriptor.write(struct.pack('<bb', 0x01, 0x00), withResponse = True)

        # No idea what this is for. Possibly a device ID of sorts? Read request returns '00 00 09 00 0c 00 02 02':
        print(" - Reading DFU2 characteristic")
        _ = self.DFU2_characteristic.read()

        # Enable API notifications:
        print(" - Writing 0x0001 to API dectriptor")
        self.API_descriptor.write(struct.pack('<bb', 0x01, 0x00), withResponse = True)

        print(" - Waking...")
        self.wake()
              
        # Finished initializing:
        print("Initialization complete")

    def disconnect(self):
        print("Disconnecting")
        self.p.disconnect()

    def wake(self):
        '''
        Bring device out of sleep mode (can only be done if device was in sleep, not deep sleep).
        If in deep sleep, the device should be connected to USB power to wake.
        '''
        self._send(characteristic=self.API_V2_characteristic,
                   devID=deviceID['powerInfo'],
                   commID=powerCommandIDs["wake"],
                   payload=[]) # empty payload

        #wait for wake acknowledgement to come in
        while(self.p.waitForNotifications(1)):
             pass

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
        self._send(characteristic = self.API_V2_characteristic,
                  devID = deviceID['userIO'],
                  commID = userIOCommandIDs["allLEDs"],
                  payload = [0x00, 0x0e, red, green, blue])

    def roll(self, speed=None, heading=None):
        '''
        Start to move the Sphero at a given direction and speed.
        heading: integer from 0 - 360 (degrees)
        speed: Integer from 0 - 255

        Note: the zero heading should be set at startup with the resetHeading method. Otherwise, it may
        seem that the sphero doesn't honor the heading argument
        '''
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

    def setBackLEDIntensity(self, brightness=None):
        '''
        Set device LED backlight intensity based on 0-255 values

        NOTE: this is not the same as aiming - it only turns on the LED
        '''
        self._send(characteristic = self.API_V2_characteristic,
                  devID = deviceID['userIO'],
                  commID = userIOCommandIDs["allLEDs"],
                  payload = [0x00, 0x01, brightness])

    def resetHeading(self):
        '''
        Reset the heading zero angle to the current heading (useful during aiming)
        '''
        self._send(characteristic = self.API_V2_characteristic,
                  devID = deviceID['driving'],
                  commID = drivingCommands["resetHeading"],
                  payload = []) #empty payload

    def returnMainApplicationVersion(self):
        '''
        Sends command to return application data in a notification
        TO DO: Parse output and print.
        '''
        self._send(self.API_V2_characteristic,
                   devID=0x11, # sys info
                   commID=0x00, # main app version
                   payload=[]) # empty

    def getBatteryVoltage(self):
        '''
        Sends command to return battery voltage data in a notification.
        Data printed to console screen by the handleNotifications() method in the MyDelegate class.
        '''
        print("Requesting battery voltage...", )
        self._send(self.API_V2_characteristic,
                   devID=0x13, # power
                   commID=0x03, # battery
                   payload=[]) # empty

        #wait for battery voltage notification to come in
        while(self.p.waitForNotifications(1)):
             pass

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

        # # DEBUG:
        # print("Sending ", output, " to ", characteristic)

        #send to specified characteristic:
        characteristic.write(output, withResponse = True)

        self.sequence += 1 # Increment sequence number (not sure that this is necessary, but probably good practice)
        if self.sequence > 255:
            self.sequence = 0

class MyDelegate(btle.DefaultDelegate):

    def __init__(self):
        btle.DefaultDelegate.__init__(self)
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
        if data == b'\xd8':
            # Once the packet is assembled, parse it:
            # Packet structure is similar to the outgoing send packets (see docstring in sphero_mini._send())
            # Check that first packet is start, and that the first bit of the second packet (flags byte)
            # indicates a response packets (see "flags")
            if data[0] != sendPacketConstants['StartOfPacket'] or not data[1] & flags['isResponse']:
                if len(self.notificationPacket) > 8: # Contains payload
                    notificationPayload = self.notificationPacket[5:-2]
                               
                # Recognize these common notifications:
                if self.notificationPacket[:4] == [141, 9, 19, 13]: # Acknowledgement after wake command
                    print(" - Wake acknowledged")

                elif self.notificationPacket[:4] == [141, 9, 19, 3]: # Sphero returning battery voltage
                    print("Battery voltage:", 
                          (notificationPayload[2] + notificationPayload[1]*256 + notificationPayload[0]*65536)/100, 
                          "v")

                # else: # default, for unrecognized commands (usually silenced)
                #      print("Packet recived: ", self.notificationPacket)

            self.notificationPacket = [] # Start new payload after this byte
