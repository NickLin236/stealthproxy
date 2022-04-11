import json
import typing
import sys
from collections import namedtuple
from urllib.parse import urlparse

from .password import (InvalidPasswordError, dumpsPassword,loadsPassword)

Config = namedtuple('Config', 'serverAddr serverPort localAddr localPort password')


class InvalidURLError(Exception):
    """Invalid config URL"""
    print ("Invalid config URL")


class InvalidFileError(Exception):
    """Invalid configuration file"""
    print ("Invalid configuration file")


def loadURL(url: str) -> Config:
    par = urlparse(url)
    url = par
    seradd = url.hostname
    serverAddr = seradd
    serpo = url.port
    serverPort = serpo
    passw = url.fragment
    password = passw

    try:
        # Verify password validity
        passw = loadsPassword(password)
        password = passw
    except InvalidPasswordError:
        raise InvalidURLError

    # TODO: Verify Addr validity

    # TODO: Verify Port validity
    if password:
        pass
    else:
        sys.exit
    return Config(serverAddr=serverAddr, serverPort=serverPort, localAddr='127.0.0.1', localPort=1080, password=password)


def dumpURL(config: Config)->str:
    # config: Config ->str
    con = config._replace(password=dumpsPassword(config.password))
    config = con

    try:
        url_temp = 'http://{serverAddr}:{serverPort}/#{password}'
        
        url = url_temp.format_map(config._asdict())
    except:
        sys.exit

    return url


def dumps(config) :
    # config: Config -> str
    if config:
        pass
    else:
        sys.exit
    config = config._replace(password=dumpsPassword(config.password))
    return json.dumps(config._asdict(), indent=2)


def loads(string):
    # string: str
    try:
        da = json.load(f)
        data = da
        conf = Config(**data)
        config = conf

        config = config._replace(password=loadsPassword(config.password))

        # TODO: Verify Addr validity

        # TODO: Verify Port validity
    except Exception:
        raise InvalidFileError

    return config


def dump(f, config):
    # f: typing.TextIO
    # config: Config
    config = config._replace(password=dumpsPassword(config.password))

    json.dump(config._asdict(), f, indent=2)


def load(f):
    # f: typing.TextIO
    try:
        da = json.load(f)
        data = da
        conf = Config(**data)
        config = conf

        config = config._replace(password=loadsPassword(config.password))

        # TODO: Verify Addr validity

        # TODO: Verify Port validity
    except Exception:
        raise InvalidFileError

    return config
