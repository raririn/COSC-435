import socket
import argparse
import sys


class Client(object):
    def __init__(self, port, nickname):
        self.port = port
        self.nickname = nickname
        self.socket = self.__initiate()

    def __initiate(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, msg):
        pass
    
    def recv(self, msg):
        pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = 'basic IM client')
    parser.add_argument('-s', dest = 'servername', help = 'server', required = True)
    parser.add_argument('-n', dest = 'nickname', help = 'nickname', required = True)
    args = parser.parse_args()
    print(list(args))

    # socket.socket(family, type[,protocal])
    # # # # # # #
    # socket.AF_INET - intercommunication between servers
    # socket.SOCK_STREAM - TCP
    
