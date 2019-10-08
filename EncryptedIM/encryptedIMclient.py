import socket
import argparse
import sys
import select
import logging
import hashlib

from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto import Random
from Crypto.Util.Padding import pad, unpad

import message_pb2

class wrappedMsg(object):
    def __init__(self, nickname, strMsg, key):
        self._nickname = nickname
        self._strMsg = strMsg
        self.key = key
        self.pack = self.encryptAndPack()

    @staticmethod
    def strToPaddedBytes(t):
        return pad(bytes(t, 'utf-8'), 16)
    
    @staticmethod
    def paddedBytesToStr(b):
        return unpad(b, 16).decode('utf-8')

    @staticmethod
    def calHMAC(authKey: bytes, msg: bytes) -> bytes:
        '''
        Calculate the HMAC for a bytes message. 
        '''
        if not isinstance(msg, bytes):
            raise TypeError('msg must be bytes.')
        h = HMAC.new(authKey, digestmod = SHA256)
        h.update(msg)
        return h.digest()
    
    def __str__(self) -> str:
        return str(self._nickname) + ":" + str(self._strMsg)
    
    def encryptAndPack(self) -> message_pb2.BasicMsg:
        ret = message_pb2.BasicMsg()
        iv = Random.new().read(AES.block_size)

        eCipher = AES.new(self.key, AES.MODE_CBC, iv)
        ret.nickname = eCipher.encrypt(self.strToPaddedBytes(self._nickname))
        ret.text = eCipher.encrypt(self.strToPaddedBytes(self._strMsg))
        ret.iv = iv

        return ret
    

    @staticmethod
    def decryptAndConstruct(packedMsg, key, encryptedHMAC):
        iv = packedMsg.iv
        dCipher = AES.new(key, AES.MODE_CBC, iv)

    
        plain_nickname = self.paddedBytesToStr(dCipher.decrypt(packedMsg.nickname))
        plain_text =  self.paddedBytesToStr(dCipher.decrypt(packedMsg.text))
        
        return wrappedMsg(plain_nickname, plain_text, key)




class Client(object):
    def __init__(self, nickname, server, serverPort = 9999, port = 80, startup = True,\
        buffer_size = 8, confKey = None, authKey = None):
        self.__port = port
        self.__nickname = nickname
        self.__server = server
        self.__serverPort = serverPort
        self.__BUFFER_SIZE = buffer_size
        if (not isinstance(confKey, bytes)) or (not isinstance(authKey, bytes)):
            raise TypeError('Keys must be hashed and in bytes format.')
        self.confKey = confKey
        self.authKey = authKey

        # WARNING: If <startup> is set to False, the program WILL COMPLAINT if attempting to run!
        if startup:
            self.socket = self.__initiate()
        else:
            self.socket = None

    @staticmethod
    def calHashForKeys(k: str) -> bytes:
        h = SHA256.new()
        h.update(bytes(k, 'utf-8'))
        return h.digest()


    def __initiate(self) -> socket.socket:
        '''
        Set up the connection and return the socket object. 
        Notice: this function should be called only ONCE!
        '''
        # AF_INET: intercommunication within servers
        # SOCK_STREAM: TCP, streaming bytes
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind('', self.__port)

        try:
            s.connect((self.__server, self.__serverPort))
        except:
            raise Exception('Connection failed.')

        return s

    def run(self) -> None:
        if not self.socket:
            raise Exception('')
        
        self.rlist = [sys.stdin, self.socket]
        self.wlist = []
        self.xlist = []

        while True:
            to_read, to_write, _ = select.select(self.rlist, self.wlist, self.xlist)

            if self.socket in to_read:
                self.recv()
        
            if sys.stdin in to_read:
                strMsg = input()
                # If the user inputs 'exit', the program shuts.
                if strMsg == 'exit':
                    self.shut()
                    # WARNING
                    quit()
                    # WARNING
                self.send(strMsg)
                print(self.__nickname + ': ' + strMsg, flush = True)
        

    def shut(self) -> None:
        ''' Close all sockets.'''
        if self.socket:
            self.socket.close()                                                                                      

    def send(self, strMsg: str) -> None:
        if not isinstance(strMsg, str):
            raise TypeError('Invalid type: the msg to be send must be str.')
        if not self.socket:
            raise Exception('Sending msg failed: No connection.')
        
        # Initialize the encryption cipher object.
        # Notice the object (and iv) is one-time.
        iv = Random.new().read(AES.block_size)
        eCipher = AES.new(self.confKey, AES.MODE_CBC, iv)

        # Initialize the message object (using protobuf).
        msg = message_pb2.BasicMsg()
        msg.nickname = self.__nickname
        msg.text = strMsg
        msg.iv = iv

        # Calculate the header (in int format).
        msg_serialized = msg.SerializeToString()
        msg_size = len(msg_serialized)

        # Message with header
        msg_w_head = msg_size.to_bytes(8, 'big') + msg_serialized

        self.socket.send(msg_w_head)
    
    def recv(self) -> None:
        if not self.socket:
            raise Exception('Receving msg failed: No connection.')

        try:
            header = self.socket.recv(self.__BUFFER_SIZE)
        except:
            logging.error("No message received!")
                   
        packagesize = int.from_bytes(header, 'big')

        try:
            data = self.socket.recv(packagesize, socket.MSG_WAITALL)
        except:
            logging.error("No message received!")

        if data:
            msg = message_pb2.BasicMsg()
            msg.ParseFromString(data)
            print(msg.nickname + ': ' + msg.text, flush = True)
        '''
        try:
            # Check https://stackoverflow.com/questions/2862071/how-large-should-my-recv-buffer-be-when-calling-recv-in-the-socket-library
            msg = self.socket.recv(self.__BUFFER_SIZE)
        except:
            raise Exception()
        
        if msg:
            sys.stdout.write(msg.nickname + ':' + msg.text + '\n')
        else:
            raise Exception()
        '''

def main() -> None:
    parser = argparse.ArgumentParser(description = 'basic IM client')
    parser.add_argument('-p', dest = 'port', help = 'port', required = True)
    parser.add_argument('-s', dest = 'servername', help = 'server', required = True)
    parser.add_argument('-n', dest = 'nickname', help = 'nickname', required = True)
    parser.add_argument('-c', dest = 'confidentialitykey', help = 'confidentialitykey', required = True)
    parser.add_argument('-a', dest = 'authenticitykey', help = 'authenticitykey', required = True)
    
    args = parser.parse_args()
    #print(args.servername, args.nickname)

    confKey = Client.calHashForKeys(args.confidentialitykey)
    authKey = Client.calHashForKeys(args.authenticitykey)    
    
    c = Client(args.nickname, args.servername, port=args.port, authKey = authKey, confKey = confKey)
    c.run()
    #c.send('123')
    c.shut()


if __name__ == "__main__":
    main()

#%%