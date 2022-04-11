from logging import *
import socket
from asyncio import *

from cipher import Cipher

flag=True
Log1 = getLogger(__name__)


class SecureSocket:
    
    #SecureSocket is the socket connection we define to both decode and encode data on server adn client side

    def __init__(self,loop,cipher):
        #
        #loop type:asyncio.Abytestring1tractEventloop
        #cipher type:Cipher
        if loop:
            self.loop=loop
        else:
            self.loop=get_event_loop() 
        self.cipher = cipher

    async def decodeRead(self,conection1):
        # conection1 type:socket.socket
        
        Data1 = await self.loop.sock_recv(conection1, 1024)

        Log1.debug('%s:%d codeblock1 %r', *conection1.getsockname(), Data1)

        bytestring1 = bytearray(Data1)
        self.cipher.decode(bytestring1)
        return bytestring1

    async def encodeWrite(self, conection1, bytestring1):
        #conection1: socket.socket
        #bytestring1: bytearray
        bytestring1_byte=bytes(bytestring1)
        Log1.debug('%s:%d codeblock11 %s', *conection1.getsockname(), bytestring1_byte)

        #bytestring1 = bytestring1.copy()

        self.cipher.encode(bytestring1)
        await self.loop.sock_sendall(conection1, bytestring1)

    async def encodeCopy(self, Destination1, Source1):
        #Destination1: socket.socket
        #Source1: socket.socket
        
        #encrypt data flow
        
        Log1.debug('codeblock2 %s:%d => %s:%d', *Source1.getsockname(), *Destination1.getsockname())

        while flag:
            if flag:
                Data1 = await self.loop.sock_recv(Source1, 1024)
            if Data1:
                pass
            else:
                break

            await self.encodeWrite(Destination1, bytearray(Data1))

    async def decodeCopy(self, Destination1, Source1):
        #Destination1: socket.socket
        #Source1: socket.socket
        #decode dataflow
        Log1.debug('codeblock22 %s:%d => %s:%d', *Source1.getsockname(), *Destination1.getsockname())

        while flag:
            if flag:
                bytestring1 = await self.decodeRead(Source1)
            if bytestring1:
                pass
            else:
                break

            await self.loop.sock_sendall(Destination1, bytestring1)