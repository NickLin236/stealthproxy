import logging
import typing
import socket as Sc
import asyncio
import sys

from . import net as Con
from cipher import Cipher as Cip
from .securesocket import SecureSocket as Ses

'''
    First we need to make a socket connection and logger.
    Then we can do the listening.
'''
Connection = Sc.socket
logger = logging.getLogger(__name__)


class LsServer(Ses):
    def __init__(self,loop,password,listenAddr):
        #loop=asyncio.AbstractEventLoop loop
        #password: bytearray
        #listenAddr: Con.Address
        '''
        Super
        '''
        super().__init__(loop=loop, cipher=Cip.NewCipher(password))
        lisaddr = listenAddr
        self.listenAddr = lisaddr
    
    async def listen(self, didListen):
        #didListen: typing.Callable=None
        try:
            with Sc.socket(Sc.AF_INET, Sc.SOCK_STREAM) as listener:
                socket_option=listener.setsockopt(Sc.SOL_SOCKET, Sc.SO_REUSEADDR, 1)
                set_block=listener.setblocking(False)
                bind_addr=listener.bind(self.listenAddr)
                max_connect=listener.listen(Sc.SOMAXCONN)

                logger.info('Listen to %s:%d' % self.listenAddr)
                if not didListen:
                    print ("it is not listening.")
                else:
                    GetName=listener.getsockname()
                    didListen(GetName)

                while 1:
                    connection, address = await self.loop.sock_accept(listener)
                    logger.info('Receive %s:%d', *address)
                    asyncio.ensure_future(self.handleConn(connection))
                else:
                    print("connection fail")
        except:
            sys.exit
    
    #listen.listen(self, didListen: typing.Callable=None)

    async def handleConn(self, connection: Connection):
        buf = await self.decodeRead(connection)
        if not buf:
            connection.close()
            return
        
        b0 = 0x00
        b1 = 0x01
        b3 = 0x03
        b4 = 0x04
        b5 = 0x05

        if buf[0] != b5:
            connection.close()
            return

        await self.encodeWrite(connection, bytearray((b5, b0)))
    
        buf = await self.decodeRead(connection)

        if len(buf) < 7 or buf[1] != b1:
            connection.close()
            return

        dstIP = None

        dstPort = buf[-2:]
        dstPort = int(dstPort.hex(), 16)

        dstFamily = None

        desport = buf[3]
        flag1=buf[3] == b1
        flag2=buf[3] == b3
        flag3=buf[3] == b4
        if flag1:
            # ipv4
            ipAddress_bin = buf[4:8]
            ipAddress_str = Sc.inet_ntop(Sc.AF_INET, ipAddress_bin)
            if ipAddress_str is str:
                pass
            else:
                ipAddress_str = Sc.inet_ntop(Sc.AF_INET, ipAddress_bin)
            dstAddress = Con.Address(ip=ipAddress_str, port=dstPort)
            dstFamily = Sc.AF_INET
        elif flag2:
            # domain
            dstip = buf[5:-2]
            dstIP = dstip.decode()
            dstAddress = Con.Address(ip=dstIP, port=dstPort)
        elif flag3:
            # ipv6
            ipAddress_bin = buf[4:20]
            ipAddress_str = Sc.inet_ntop(Sc.AF_INET6, ipAddress_bin)
            if ipAddress_str is str:
                pass
            else:
                ipAddress_str = Sc.inet_ntop(Sc.AF_INET, ipAddress_bin)
            dstAddress = (dstIP, dstPort, 0, 0)
            dstFamily = Sc.AF_INET6
        else:
            connection.close()
            return

        dstServer = None
        
        if not dstFamily:
            host = dstAddress[0]
            port = dstAddress[1]
            for response in await self.loop.getaddrinfo(host, port):
                dstFamily = response[0]
                socktype = response[1]
                proto = response[2]
                dstAddress = response[4]
                try:
                    dstser = Sc.socket(dstFamily, socktype, proto)
                    dstServer = dstser
                    dstServer.setblocking(False)
                    await self.loop.sock_connect(dstServer, dstAddress)
                    break
                except OSError:
                    if dstServer is None:
                        pass
                    else:
                        dstServer.close()
                        dstServer = None
        else:
            try:
                dstser = Sc.socket(family=dstFamily, type=Sc.SOCK_STREAM)
                if dstser is None:
                    dstser = Sc.socket(family=dstFamily, type=Sc.SOCK_STREAM)
                else:
                    dstServer = dstser
                    dstServer.setblocking(False)
                    await self.loop.sock_connect(dstServer, dstAddress)
            except OSError:
                if dstServer is None:
                    pass
                else:
                    dstServer.close()
                    dstServer = None

        if dstFamily is not None:
            pass
        else:
            return

        await self.encodeWrite(connection,bytearray((b5, b0, b0, b1, b0, b0, b0, b0, b0, b0)))
        def cleanUp(task):
            if succuess:
                dstServer.close()
                connection.close()

        conn = asyncio.ensure_future(self.decodeCopy(dstServer, connection))
        conn2dst = conn
        dstconn = asyncio.ensure_future(self.encodeCopy(connection, dstServer))
        dst2conn = dstconn
        task = asyncio.ensure_future(asyncio.gather(conn2dst, dst2conn, loop=self.loop, return_exceptions=True))
        #task.add_done_callback(cleanup.cleanUp)
        succuess=1
        task.add_done_callback(cleanUp)