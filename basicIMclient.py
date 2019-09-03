import socket
import argparse
import sys

import message_pb2


class Client(object):
    def __init__(self, port, nickname):
        self.port = port
        self.nickname = nickname
        self.socket = self.__initiate()

    def __initiate(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, strMsg):
        if not self.socket:
            raise Exception('')
        
        msg = message_pb2.BasicMsg()
        msg.nickname = self.nickname
        msg.message = strMsg

        
    
    def recv(self, strMsg):
        if not self.socket:
            raise Exception('')

        pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = 'basic IM client')
    parser.add_argument('-s', dest = 'servername', help = 'server', required = True)
    parser.add_argument('-n', dest = 'nickname', help = 'nickname', required = True)
    args = parser.parse_args()
    print(args.servername, args.nickname)

    # socket.socket(family, type[,protocal])
    # # # # # # #
    # socket.AF_INET - intercommunication between servers
    # socket.SOCK_STREAM - TCP
    
    
    c = Client(args.servername, args.nickname)
