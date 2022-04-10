import time
import random
import sys
import base64

IDENTITY_PASSWORD = bytearray(range(256))


class InvalidPasswordError(Exception):
    '''give exception for invalid password'''


def validatePassword(password: bytearray) -> bool:
    if len(password) == 256:
        if len(set(password)) == 256:
            return True
        else:
            return False
    else:
        return False


def loadsPassword(passwordString: str) -> bytearray:
    try:
        passenocde = passwordString.encode('utf8', errors='strict')
        password = bytearray(base64.urlsafe_b64decode(passenocde))
        #password = bytearray(password)
    except:
        raise InvalidPasswordError

    if validatePassword(password):
        return password
    else:
        raise InvalidPasswordError
        

def dumpsPassword(password: bytearray) -> str:
    if validatePassword(password):
        dumpass = base64.urlsafe_b64encode(password).decode('utf8', errors='strict')
        #dumpass = str(dumpass)
        return dumpass
    else:
        raise InvalidPasswordError

def randomPassword() -> bytearray:
    password = IDENTITY_PASSWORD.copy()
    random.shuffle(password)
    return password
