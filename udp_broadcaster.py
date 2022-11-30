from socket import *


class Broadcast:
    def __init__(self, mac, port):
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.mac_address = mac
        self.broadcast_port = port
        data = '"sensor": "' + self.mac_address + '", "message": "Sensor Ready."'
        self.broadcast(data)

    def broadcast(self, data):
        if data:
            print("(" + str(self.broadcast_port) + ") Broadcast: " + data + "")
            self.s.sendto(data.encode(), ("255.255.255.255", self.broadcast_port))
