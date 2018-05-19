'''
Known Peripheral UUIDs, obtained by querying using the Bluepy module:
=====================================================================
Anti DOS Characteristic <00020005-574f-4f20-5370-6865726f2121>
Battery Level Characteristic <Battery Level>
Peripheral Preferred Connection Parameters Characteristic <Peripheral Preferred Connection Parameters>
API V2 Characteristic <00010002-574f-4f20-5370-6865726f2121>
DFU Control Characteristic <00020002-574f-4f20-5370-6865726f2121>
Name Characteristic <Device Name>
Appearance Characteristic <Appearance>
DFU Info Characteristic <00020004-574f-4f20-5370-6865726f2121>
Service Changed Characteristic <Service Changed>
Unknown1 Characteristic <00020003-574f-4f20-5370-6865726f2121>
Unknown2 Characteristic <00010003-574f-4f20-5370-6865726f2121>

The rest of the values saved in the dictionaries below, were borrowed from
@igbopie's javacript library, which is available at https://github.com/igbopie/spherov2.js
'''

deviceID = {"apiProcessor": 16,
            "systemInfo": 17,
            "powerInfo": 19,
            "driving": 22,
            "animatronics": 23,
            "sensor": 24,
            "userIO": 26,
            "somethingAPI": 31}

SystemInfoCommands = {"mainApplicationVersion": 0x00,
                      "bootloaderVersion": 0x01,
                      "something": 0x06,
                      "something6": 0x12,
                      "something7": 0x28}

sendPacketConstants = {"StartOfPacket": 0x8D,
                       "EndOfPacket": 0xD8}

userIOCommandIDs = {"allLEDs": 14,
                   "playAudioFile": 7,
                   "audioVolume": 8,
                   "stopAudio": 10,
                   "testSound": 24}

flags= {"isResponse": 1,
        "requestsResponse": 2,
        "requestsOnlyErrorResponse": 4,
        "resetsInactivityTimeout": 8}

# Do not edit the order of the list here:
characteristicNames=["Name",
                     "Appearance",
                     "Peripheral Preferred Connection Parameters",
                     "Service Changed",
                     "Unknown1",
                     "DFU Control",
                     "DFU Info",
                     "Anti DOS",
                     "Battery Level",
                     "API V2",
                     "Unknown2"]

powerCommandIDs={"deepSleep": 0x00,
                "sleep": 0x01,
                "batteryVoltage": 0x03,
                "wake": 0x0D,
                "something2": 0x10,
                "something3": 0x04,
                "something4": 0x1E}

drivingCommands={"rawMotor": 0x01,
                 "resetYaw": 0x06,
                 "driveAsSphero": 0x04,
                 "driveAsRc": 0x02,
                 "driveWithHeading": 0x07,
                 "stabilization": 0x0C}

'''
TBD: Incorporate info from igbopie's javascript lib:

Animatronics:
    animationBundle = 5
    shoulderAction = 13
    domePosition = 15
    shoulderActionComplete = 38
    enableShoulderActionCompleteAsync = 42

Sensor Commands:
    sensorMask = 0
    sensorResponse = 2
    configureCollision = 17
    collisionDetectedAsync = 18
    resetLocator = 19
    enableCollisionAsync = 20
    sensor1 = 15
    sensor2 = 23
    configureSensorStream = 12
'''
