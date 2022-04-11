import argparse as Argp
import asyncio as Aio
import sys
from threading import local

from support.password import InvalidPasswordError, loadsPassword
from support.localhandle import Localhandle as Lh
import support.config  as Fig
import support.net as Connect
#yang guo
#yga105@sfu.ca

def run_server(setting: Fig.Config):
    lop = Aio.get_event_loop()
    locAdr=setting.localAddr
    locPort=setting.localPort
    servAddr=setting.serverAddr
    servPort=setting.serverPort
    passwd=setting.password

    ldr = Connect.Address(locAdr, locPort)
    rdr = Connect.Address(servAddr,servPort)
    sev = Lh(loop=lop,password=passwd,listenAddr=ldr,remoteAddr=rdr)
    if ldr:
        if locPort:
            print('Listen to %s:%d\n' % (locAdr,locPort))
    def Listening(address):
        print("listening")
    Aio.ensure_future(sev.listen(Listening))
    lop.run_forever()


def main():
    structconfig = Argp.ArgumentParser(description='modify shadowsocks')
    structconfig1=structconfig.add_argument('--version',action='store_true',default=False,help='show version information')

    options = structconfig.add_argument_group('options')

    option1=options.add_argument('--save', metavar='CONFIG', help='path to dump config')
    option2=options.add_argument('-c', metavar='CONFIG', help='path to config file')
    option3=options.add_argument('-u',metavar='URL',help='url contains server address, port and password')
    option4=options.add_argument('-s', metavar='SERVER_ADDR', help='server address')
    option5=options.add_argument('-p',metavar='SERVER_PORT',type=int,help='server port, default: 8388')
    option6=options.add_argument('-b',metavar='LOCAL_ADDR',help='local binding address, default: 127.0.0.1')
    option7=options.add_argument('-l', metavar='LOCAL_PORT', type=int, help='local port, default: 1080')
    option8=options.add_argument('-k', metavar='PASSWORD', help='password')

    args = structconfig.parse_args()
    GetVersion=args.version
    GetConfig=args.c
    GetUrl=args.u
    GetServerAddr=args.s
    GetServerPort=args.p
    GetLocalAddr=args.b
    GetLocalPort=args.l
    GetPassword=args.k
    GetSave=args.save


    if GetVersion:
        print('lightsocks 0.1.0')
        sys.exit(0)

    config = Fig.Config(None, None, None, None, None)
    if GetConfig:
        try:
            if config:
                with open(GetConfig, encoding='utf-8') as file1:
                    file_config = Fig.load(file1)
        except :
            if Fig.InvalidFileError:
                structconfig.print_usage()
                print(f'invalid config file {GetConfig!r}')
            if FileNotFoundError:
                structconfig.print_usage()
                print(f'config file {GetConfig!r} not found')
            sys.exit(1)

        config = config._replace(**file_config._asdict())

    if GetUrl:
        try:
            url_config = Fig.loadURL(GetUrl)
        except:
            structconfig.print_usage()
            if Fig.InvalidURLError:
                print(f'invalid url {GetUrl!r}')
                sys.exit(1)

        config = config._replace(**url_config._asdict())

    if GetServerAddr:
        config = config._replace(serverAddr=GetServerAddr)

    if GetServerPort:
        config = config._replace(serverPort=GetServerPort)

    if GetLocalAddr:
        config = config._replace(localAddr=GetLocalAddr)

    if GetLocalPort:
        config = config._replace(localPort=GetLocalPort)

    if GetPassword:
        try:
            pwd = loadsPassword(GetPassword)
            config = config._replace(password=pwd)
        except InvalidPasswordError:
            structconfig.print_usage()
            print('invalid password')
            sys.exit(1)
    no_ldr=config.localAddr is None
    no_lpo=config.localPort is None
    no_pwd=config.password is None
    no_sdr=config.serverAddr is None
    no_spo=config.serverPort is None
    no_ags=GetSave is None
    if no_ldr:
        config = config._replace(localAddr='127.0.0.1')

    if no_lpo:
        config = config._replace(localPort=1080)

    if no_spo:
        config = config._replace(serverPort=8388)

    if no_pwd is None:
        structconfig.print_usage()
        print('need PASSWORD, please use [-k PASSWORD]')
        sys.exit(1)

    if no_sdr is None:
        structconfig.print_usage()
        print('need SERVER_ADDR, please use [-s SERVER_ADDR]')

    if no_ags:
        pass
    else:
        print(f'dump config file into {GetSave!r}')
        with open(GetSave, 'w', encoding='utf-8') as f:
            Fig.dump(f, config)

    run_server(config)


if __name__ == '__main__':
    main()
