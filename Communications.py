import socket
import serial
import time

class CommsObject:
    def __init__(self, name = "", type = ""):
        self.name = name
        self.type = type
        self.forwardList = []

    def sendMessage(self):
        return True

    def recvMessage(self):
        return None, False

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def openCom(self):
        return 0

    def closeCom(self):
        return 0

class SerialObject(CommsObject):
    def __init__(self, name, port = "COM1", baud = 9600):
        super().__init__(name, "Serial")
        self.port = port
        self.baud = baud
        self.ser = None

    def openCom(self):
        self.ser = serial.Serial(self.port, self.baud)

    def closeCom(self):
        self.ser.close()

    def sendMessage(self, message):
        bwr = 0
        try:
            bwr = self.ser.write(message)
        except:
            bwr = self.ser.write(message.encode('utf-8'))
        return bwr > 0

    def recvMessage(self):
        time.sleep(.2)
        msg = self.ser.read(self.ser.in_waiting)
        try:
            msg = msg.decode('utf-8')
        except:
            if len(msg) == 0:
                return "", False
        return msg, True


    def setPort(self, port):
        self.port = port

    def setBaud(self, baud):
        self.baud = baud

    def getPort(self):
        return self.port

    def getBaud(self):
        return self.baud

class UDPObject(CommsObject):

    def __init__(self, name, IP = "192.168.1.1", Port = 8000):
        super().__init__(name, "UDP")
        self.IP = IP
        self.Port = Port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bufferLen = 1024
        self.lastAddr = None

    def sendMessage(self, message):
        print("Send Message: " + message)
        self.sock.sendto(message.encode('utf-8'), (self.IP, self.Port))

    def recvMessage(self):
        success = True
        data, addr = self.sock.recvfrom(self.bufferLen)
        if data == None:
            success = False
        else:
            self.lastAddr = addr
        return data, success

    def setIP(self, IP):
        self.IP = IP

    def setPort(self, Port):
        self.Port = Port

    def openCom(self):
        self.sock.bind((self.IP, self.Port))

    def closeCom(self):
        self.sock.close()

    def setBufferLen(self, bufferLen):
        self.bufferLen = bufferLen

    def getIP(self):
        return self.IP

    def getPort(self):
        return self.Port

    def getBufferLen(self):
        return self.bufferLen



class TCPObject(CommsObject):
    def __init__(self, name, IP = "192.168.1.1", Port = 8000):
        super().__init__(name, "UDP")
        self.IP = IP
        self.Port = Port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bufferLen = 1024
        self.lastAddr = None

    def sendMessage(self, message):
        self.sock.sendto(message, (self.IP, self.Port))

    def recvMessage(self):
        success = True
        data, addr = self.sock.recvfrom(self.bufferLen)
        if data == None:
            success = False
        else:
            self.lastAddr = addr
        return data, success

    def setIP(self, IP):
        self.IP = IP

    def setPort(self, Port):
        self.Port = Port

    def openCom(self):
        self.sock.connect((self.IP, self.Port))

    def closeCom(self):
        self.sock.close()

    def setBufferLen(self, bufferLen):
        self.bufferLen = bufferLen

    def getIP(self):
        return self.IP

    def getPort(self):
        return self.Port

    def getBufferLen(self):
        return self.bufferLen


class Communications:

    def __init__(self):
        self.commsObjects = []
        self.updateObjects = []

    def newComPort(self, name, type, args = []):
        newObj = None
        if type == "UDP":
            if len(args) == 2:
                newObj = UDPObject(name, args[0], args[1])
            else:
                newObj = UDPObject(name)
        elif type == "Serial":
            if (len(args) == 2):
                newObj = SerialObject(name, args[0], args[1])
            else:
                newObj = SerialObject(name)
        elif type == "TCP":
            newObj = TCPObject(name)
        self.commsObjects.append(newObj)

    def sendMessage(self, name, message):
        for i in range(len(self.commsObjects)):
            if self.commsObjects[i].name == name:
                self.commsObjects[i].sendMessage(message)
                return
