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

deviceID = {"apiProcessor": 0x10,   # 16
            "systemInfo": 0x11,     # 17
            "powerInfo": 0x13,      # 19
            "driving": 0x16,        # 22
            "animatronics": 0x17,   # 23
            "sensor": 0x18,         # 24
            "something": 0x19,      # 25
            "userIO": 0x1a,         # 26
            "somethingAPI": 0x1f}   # 31

SystemInfoCommands = {"mainApplicationVersion": 0x00,
                      "bootloaderVersion": 0x01,
                      "something": 0x06,
                      "something": 0x13,
                      "something6": 0x12,
                      "something7": 0x28} # 40

sendPacketConstants = {"StartOfPacket": 0x8D,
                       "EndOfPacket": 0xD8}

userIOCommandIDs = {"allLEDs": 0x0e} # 14

flags= {"isResponse": 1,
        "requestsResponse": 2,
        "requestsOnlyErrorResponse": 4,
        "resetsInactivityTimeout": 8}

powerCommandIDs={"deepSleep": 0x00,
                "sleep": 0x01,
                "batteryVoltage": 0x03,
                "wake": 0x0D,           #13
                "something2": 0x10,
                "something3": 0x04,
                "something4": 0x1E}

drivingCommands={"rawMotor": 0x01,
                 "resetHeading": 0x06,
                 "driveAsSphero": 0x04,
                 "driveAsRc": 0x02,
                 "driveWithHeading": 0x07,
                 "stabilization": 0x0C}

'''
TO DO: Incorporate info from igbopie's javascript lib:

Animatronics: # Not sure if these all apply to the mini - some might apply to the BB9, etc
    animationBundle = 5
    shoulderAction = 13
    domePosition = 15
    shoulderActionComplete = 38
    enableShoulderActionCompleteAsync = 42

Sensor Commands:
    sensorMask = 0
    sensorResponse = 2
    configureCollision = 0x11         # 17
    collisionDetectedAsync = 18
    resetLocator = 19
    enableCollisionAsync = 20
    sensor1 = 0x0F,                   # 15
    sensor2 = 23
    configureSensorStream = 0x0C      # 12
'''
