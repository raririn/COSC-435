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
        #self.client_list = []
        self.msg_buffer = []
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

        addr_list = []

        #conn, addr = self.socket.accept()
        
        # These attributes are only defined and used in THIS scope.
        self.rlist = [self.socket]
        self.wlist = []
        self.xlist = []

        count = 0
        while True:
            #print(count)
            count = count + 1
            #print(self.rlist, self.wlist, self.xlist)
            to_read, to_write, exc = select.select(self.rlist, self.wlist, self.xlist)

            #if not to_read:
            #    raise Exception('')
            

            # Read handles
            if self.socket in to_read:
                conn, addr = self.socket.accept()
                self.rlist.append(conn)
                addr_list.append(addr)

            for c in to_read:
                if not c is self.socket:
                    # header and data are both <bytes> object
                    try:
                        header = c.recv(self.__BUFFER_SIZE)
                    except:
                        logging.error("No message received!")
                    
                    packagesize = int.from_bytes(header, 'big')

                    try:
                        data = c.recv(packagesize, socket.MSG_WAITALL)
                    except:
                        logging.error("No message received!")

                    if data:
                        msg = message_pb2.BasicMsg()
                        msg.ParseFromString(data)
                        print(msg.text)

                        self.msg_buffer = header + data
                        self.wlist.append(c)
                        header = None
                        data = None
                    
                    else:
                        if c in self.rlist:
                            self.rlist.remove(c)
                        c.close()

            # Write handles
            if to_write:
                print("exc")
                print(self.rlist)
                for i in to_write:
                    for j in self.rlist:
                        if (not j is self.socket) and (not j is i):
                            try:
                                j.send(self.msg_buffer)
                            except:
                                #i.close()
                                pass
                self.msg_buffer = None
                self.wlist = []

            
            
            

if __name__ == "__main__":
    s = Server()