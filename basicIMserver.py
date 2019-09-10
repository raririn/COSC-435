import socket
import select
import logging
import sys

import message_pb2

class Server(object):
    def __init__(self, host = 'localhost', port = 9999, buffer_size = 8, startup = True, queue_num = 5):
        if not (isinstance(host, str) and isinstance(port, int) and isinstance(buffer_size, int)):
            raise TypeError('')
        self.__host = host
        self.__port = port
        self.__BUFFER_SIZE = buffer_size
        self.__queue_num = queue_num
        if startup:
            self.socket = self.__initiate()
            self.__loop()

    def run(self):
        if startup:
            return
        self.socket = self.__initiate()
        self.__loop()

    def __initiate(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(('', self.__port))

            # src: https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.2.0/com.ibm.zos.v2r2.bpxbd00/listen.htm
            # int listen(int socket, int backlog);
            # # # # # # #
            # backlog: Defines the maximum length for the queue of pending connections.
            # The listen() call indicates a readiness to accept
            # client connection requests. It transforms an active
            # socket into a passive socket. Once called, socket can 
            # never be used as an active socket to initiate connection 
            # requests. Calling listen() is the third of four steps that
            # a server performs to accept a connection. It is called after
            # allocating a stream socket with socket(), and after binding
            # a name to socket with bind(). It must be called before calling accept().
            # If the backlog is less than 0, backlog is set to 0. 
            # If the backlog is greater than SOMAXCONN, as defined in sys/socket.h, backlog is set to SOMAXCONN.
            s.listen(1)
        except:
            raise Exception('')

        print("Start listening on " + self.__host + ":" + str(self.__port))
        #conn, addr = s.accept()
        return s

    def __loop(self):
        if not self.socket:
            raise Exception('')

        conn, addr = self.socket.accept()
        rlist = [sys.stdin, conn]
        wlist = []
        xlist = []

        while True:
            to_read, to_write, exc = select.select(rlist, wlist, xlist)

            if not to_read:
                raise Exception('')

            
            if conn in to_read:
                try:
                    data = conn.recv(self.__BUFFER_SIZE)
                except:
                    logging.error("No message received!")
                
                packagesize = int.from_bytes(data, 'big')
                try:
                    data = conn.recv(packagesize)
                except:
                    logging.error("No message received!")

                if data:
                    msg = message_pb2.BasicMsg()
                    msg.ParseFromString(data)
                    print(msg.text)
                    data = None
            

            if addr:
                print(str(addr))
                addr = None
            
            

if __name__ == "__main__":
    s = Server()