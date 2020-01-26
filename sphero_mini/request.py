import struct
import response


class Request(object):
    SOP1 = 0xFF
    SOP2 = 0xFF
    did = 0x00
    cid = 0x00
    fmt = None

    def __init__(self, seq=0x00, *data):
        self.seq = seq
        self.data = data
        if not self.fmt:
            self.fmt = '%sB' % len(self.data)

    def __str__(self):
        return self.bytes

    def checksum(self):
        body = self.packet_header() + self.packet_body()
        body = struct.unpack('%sB' % len(body), body)
        return struct.pack('B', ~(sum(body[2:]) % 256) & 0xFF)

    @property
    def bytes(self):
        return self.packet_header() + self.packet_body() + self.checksum()

    def packet_header(self):
        return struct.pack('6B', *self.header())

    def packet_body(self):
        if not self.data:
            return ''
        return struct.pack(self.fmt, *self.data)

    @property
    def dlen(self):
        return struct.calcsize(self.fmt) + 1

    def header(self):
        return [self.SOP1, self.SOP2, self.did, self.cid, self.seq, self.dlen]

    def response(self, header, body):
        """
        :param header: The header of the received response msg
        :param body: The body of the received response msg
        :return: Returns a given response type
        :rtype: response.Response
        """
        name = self.__class__.__name__.split('.')[-1]
        klass = getattr(response, name, response.Response)
        return klass(header, body)


class Core(Request):
    did = 0x00


class Ping(Core):
    cid = 0x01


class GetVersion(Core):
    cid = 0x02


class SetDeviceName(Core):
    cid = 0x10


class GetBluetoothInfo(Core):
    cid = 0x11


class GetAutoReconnect(Core):
    cid = 0x12


class SetAutoReconnect(Core):
    cid = 0x13


class GetPowerState(Core):
    cid = 0x20


class SetPowerNotification(Core):
    cid = 0x21


class Sleep(Core):
    cid = 0x22


class GetVoltageTripPoints(Core):
    cid = 0x23


class SetVoltageTripPoints(Core):
    cid = 0x24


class SetInactivityTimeout(Core):
    cid = 0x25


class JumpToBootloader(Core):
    cid = 0x30


class PerformLevel1Diagnostics(Core):
    cid = 0x40


class PerformLevel2Diagnostics(Core):
    cid = 0x41


class ClearCounters(Core):
    cid = 0x42


class SetTimeValue(Core):
    cid = 0x50


class PollPacketTimes(Core):
    cid = 0x51


#Sphero Commands

class Sphero(Request):
    did = 0x02


class SetHeading(Sphero):
    cid = 0x01
    fmt = '!H'


class SetStabilization(Sphero):
    cid = 0x02


class SetRotationRate(Sphero):
    cid = 0x03


class SetApplicationConfigurationBlock(Sphero):
    cid = 0x04


class GetApplicationConfigurationBlock(Sphero):
    cid = 0x05


class ReenableDemoMode(Sphero):
    cid = 0x06


class GetChassisId(Sphero):
    cid = 0x07


class SetChassisId(Sphero):
    cid = 0x08


class SelfLevel(Sphero):
    cid = 0x09


class SetVDL(Sphero):
    cid = 0x0A


class SetDataStreaming(Sphero):
    fmt = '!2HIBI'
    cid = 0x11


class ConfigureCollisionDetection(Sphero):
    cid = 0x12


class ConfigureLocator(Sphero):
    fmt = '!b3h'
    cid = 0x13


class SetAccelerometer(Sphero):
    cid = 0x14


class ReadLocator(Sphero):
    cid = 0x15


class SetRGB(Sphero):
    cid = 0x20


class SetBackLEDOutput(Sphero):
    cid = 0x21


class GetRGB(Sphero):
    cid = 0x22


class Roll(Sphero):
    fmt = '!BHB' #Speed, heading, state
    cid = 0x30


class SetBoostWithTime(Sphero):
    fmt = '!?'
    cid = 0x31


class SetRawMotorValues(Sphero):
    cid = 0x33


class SetMotionTimeout(Sphero):
    fmt = '!H'
    cid = 0x34


class SetOptionFlags(Sphero):
    fmt = '!i'
    cid = 0x35


class GetOptionFlags(Sphero):
    cid = 0x36


class GetConfigurationBlock(Sphero):
    cid = 0x40


class GetDeviceMode(Sphero):
    cid = 0x42


class RunMacro(Sphero):
    cid = 0x50


class SaveTemporaryMacro(Sphero):
    cid = 0x51


class ReinitMacro(Sphero):
    cid = 0x54


class AbortMacro(Sphero):
    cid = 0x55


class GetMacroStatus(Sphero):
    cid = 0x56


class SetMacroParameter(Sphero):
    cid = 0x57


class AppendMacroChunk(Sphero):
    cid = 0x58


class EraseOrbbasicStorage(Sphero):
    cid = 0x60


class AppendOrbbasicFragment(Sphero):
    cid = 0x61


class RunOrbbasicProgram(Sphero):
    cid = 0x62


class AbortOrbbasicProgram(Sphero):
    cid = 0x63


class AnswerInput(Sphero):
    cid = 0x64