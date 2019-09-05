import socket
import argparse
import sys
import logging

import message_pb2


class Client(object):
    def __init__(self, nickname, server, serverPort = 9999, port = 80, startup = True, buffer_size = 1024):
        self.__port = port
        self.__nickname = nickname
        self.__server = server
        self.__serverPort = serverPort
        self.__BUFFER_SIZE = buffer_size
        if startup:
            self.socket = self.__initiate()

    def __initiate(self):
        '''
        Set up the connection. Notice: this function should be
        called only ONCE!
        '''
        # AF_INET: intercommunication within servers
        # SOCK_STREAM: TCP, streaming bytes
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.bind('', self.__port)

        try:
            s.connect((self.__server, self.__serverPort))
        except:
            raise Exception('Connection failed.')

        return s

    def __run(self):
        if startup:
            return
        self.socket = self.__initiate()

    def shut(self):
        if self.socket:
            self.socket.close()                                                                                         

    def send(self, strMsg):
        if not isinstance(strMsg, str):
            raise TypeError('')
        if not self.socket:
            raise Exception('Sending msg failed: No connection.')
        
        msg = message_pb2.BasicMsg()
        msg.nickname = self.__nickname
        msg.text = strMsg

        self.socket.send(msg.SerializeToString())
    
    def recv(self, strMsg):
        if not self.socket:
            raise Exception('Receving msg failed: No connection.')

        try:
            # Check https://stackoverflow.com/questions/2862071/how-large-should-my-recv-buffer-be-when-calling-recv-in-the-socket-library
            msg = self.socket.recv(self.__BUFFER_SIZE)
        except:
            raise Exception()
        
        if msg:
            sys.stdout.write(msg.nickname + ':' + msg.text + '\n')
        else:
            raise Exception()
        
        

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
    
    
    c = Client(args.nickname, args.servername)
    c.send('123')
    c.shut()