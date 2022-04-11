import typing
import socket as Sc
import asyncio
import sys
import logging

from . import net as Con
from .cipher import Cipher as Cip
from .securesocket import SecureSocket as Ses

'''
    First we need to make a socket connection and logger.
    Then we can do the listening.
'''
Connection = Sc.socket
logger = logging.getLogger(__name__)


class Localhandle(Ses):
    def __init__(self, loop, password, listenAddr, remoteAddr):
        # loop : asyncio.AbstractEventLoop
        # password : bytearray
        # listenAddr : net.Address
        # remoteAddr : net.Address
        super().__init__(loop=loop, cipher=Cip.NewCipher(password))
        lisaddr = listenAddr
        self.listenAddr = lisaddr
        readdr = remoteAddr
        self.remoteAddr = readdr

    async def listen(self, didListen):
        # didListen: typing.Callable=None
        try:
            with Sc.socket(Sc.AF_INET, Sc.SOCK_STREAM) as listener:
                socket_option = listener.setsockopt(Sc.SOL_SOCKET, Sc.SO_REUSEADDR, 1)
                set_block = listener.setblocking(False)
                bind_addr = listener.bind(self.listenAddr)
                max_connect = listener.listen(Sc.SOMAXCONN)
                

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

    #listen.listen(self, didListen)

    async def handleConn(self, connection):
        # connection: Connection
        remoteServer = await self.dialRemote()
        def cleanUp(task):
            if success:
                remoteServer.close()
                connection.close()

        ltore = asyncio.ensure_future(self.decodeCopy(connection, remoteServer))
        local2remote = ltore
        retol = asyncio.ensure_future(self.encodeCopy(remoteServer, connection))
        remote2local = retol
        task = asyncio.ensure_future(asyncio.gather(local2remote, remote2local, loop=self.loop, return_exceptions=True))
        success=1
        task.add_done_callback(cleanUp)

    async def dialRemote(self):
        try:
            reconn = Sc.socket(Sc.AF_INET, Sc.SOCK_STREAM)
            remoteConn = reconn
            remoteConn.setblocking(False)
            if remoteConn.setblocking(False):
                pass
            else:
                sys.exit
            await self.loop.sock_connect(remoteConn, self.remoteAddr)
        except Exception as error:
            raise ConnectionError('Connect to remote server %s:%d fail:\n%r' % (*self.remoteAddr, error))
        return remoteConn
