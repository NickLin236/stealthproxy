from collections import namedtuple
import socket
import asyncio
import sys
import logging
#socket connection
Connection = socket.socket
#logger
logger = logging.getLogger()
#namedtuple
Address = namedtuple('Address', 'ip port')