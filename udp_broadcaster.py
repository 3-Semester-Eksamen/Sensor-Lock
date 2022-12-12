from socket import *


class Broadcast:
    def __init__(self, port):
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.broadcast_port = port

    def broadcast(self, data):
        if data:
            print("(" + str(self.broadcast_port) + ") Broadcast: " + data + "")
            self.s.sendto(data.encode(), ("255.255.255.255", self.broadcast_port))
