import argparse as Argp
import asyncio as Aio
import sys

from support.password import (InvalidPasswordError, dumpsPassword,loadsPassword, randomPassword)
from support.serverhandle import Serverhandle as Sh
import support.config as Fig
import support.net as Connect
#yang guo
#yga105@sfu.ca

def run_server(Setting):
    #Setting belongs to class Fig.Config
    lop = Aio.get_event_loop()
    sevAdr=Setting.serverAddr
    sevPot=Setting.serverPort
    pwd=Setting.password
    ldr = Connect.Address(sevAdr, sevPot)
    sev = Sh(loop=lop, password=pwd, listenAddr=ldr)
    print('server address is '+ sevAdr)
    print('replace 127.0.0.1 with actual hostname if connected in internet\n')
    print('''python3 lslocal.py -u "http://127.0.0.1:8388/#'''f'''{dumpsPassword(Setting.password)}"''')
    print('\n Setting lslocal')

    Aio.ensure_future(sev.listen())
    lop.run_forever()


def main():
    struct = Argp.ArgumentParser(description='shadowsocks implements server')
    struct.add_argument('--version',action='store_true',default=False,help='show version information')

    options = struct.add_argument_group('Proxy options')
    option1=options.add_argument('--save', metavar='Setting', help='save setting')
    option2=options.add_argument('-c', metavar='Setting', help='setting files location')
    option3=options.add_argument('-s', metavar='SERVER_ADDR', help='the address server listen to, default: 0.0.0.0')
    option4=options.add_argument('-p',metavar='SERVER_PORT',type=int,help='the port listen to, shadowsocks server use 8388 in default')
    option5=options.add_argument('-k', metavar='PASSWORD', help='password')
    option6=options.add_argument('--random',action='store_true',default=False,help='initialize a random password')

    args = struct.parse_args()
    GetVersion=args.version
    Getconfig=args.c
    GetServerAddr=args.s
    GetServerPort=args.p
    GetPassword=args.k
    GetSave=args.save
    GetRando=args.random
    NoRando=not GetRando
    if GetVersion:
        print('shadowsock implements')
        sys.exit(0)

    Setting = Fig.Config(None, None, None, None, None)
    if Getconfig:
        try:
            with open(Getconfig, encoding='utf-8') as file1:
                file_Setting = Fig.load(file1)
        except: 
            usage1=struct.print_usage()
            if Fig.InvalidFileError:
                print(f'setting file error:{Getconfig!r}') 
            if FileNotFoundError:
                print(f'Setting file {Getconfig!r} does not exist')
            sys.exit(1)
        Setting = Setting._replace(**file_Setting._asdict())

    if GetServerAddr:
        Setting = Setting._replace(serverAddr=GetServerAddr)
    if GetServerPort:
        Setting = Setting._replace(serverPort=GetServerPort)
    if GetPassword:
        try:
            pwd= loadsPassword(GetPassword)
            Setting = Setting._replace(password=pwd)
        except InvalidPasswordError:
            struct.print_usage()
            print('password error')
            sys.exit(1)
    sdr=Setting.serverAddr
    sdrEmpty=sdr is None
    if  sdrEmpty:
        Setting = Setting._replace(serverAddr='0.0.0.0')
    spt=Setting.serverPort
    sptEmpty=spt is None 
    if sptEmpty:
        Setting = Setting._replace(serverPort=8388)
    pwdEmpty=Setting.password is None
    if pwdEmpty:
        if NoRando:
            struct.print_usage()
            print('please incluse a password, -k can be use to connect with an existing password or --random can generate a random password')
            sys.exit(1)

    if GetRando:
        print('randomly initial with a password')
        Setting = Setting._replace(password=randomPassword())

    if GetSave:
        print(f'Setting is save to {GetSave!r}')
        with open(GetSave, 'w', encoding='utf-8') as file2:
            Fig.dump(file2, Setting)

    run_server(Setting)


if __name__ == '__main__':
    main()
