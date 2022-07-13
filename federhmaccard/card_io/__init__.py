#!/usr/bin/env python3

from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
import hashlib
from .crypto import crypto_encrypt, crypto_decrypt


from .commands._prototype import *
from .commands.FC_GET_CHALLENGE     import * 
from .commands.FC_VERIFY            import * 
from .commands.FC_VAULT_OPEN        import *
from .commands.FC_VAULT_STATUS      import *
from .commands.FC_VAULT_IMPORT      import *
from .commands.FC_VAULT_REENCRYPT   import *
from .commands.FC_VAULT_HMAC_SHA1   import *
from .commands.FC_VAULT_HMAC_SHA256 import *
from .commands.FC_VAULT_CLOSE       import *



"""
declare command &H88 &H88 FACTORY_INIT(LC=0, data as string)
declare command &H88 &H86 FC_FACTORY_RESET(data as string)

declare command &H88 &H00 Greet(LC=0, data as string)

declare command &H88 &H84 FC_GET_CHALLENGE(LC=0, data as string)
declare command &H88 &H20 FC_VERIFY(data as string)


declare command &H84 &H24 FC_CHANGE_PASSWORD(data as string)


declare command &H84 &H00 FC_VAULT_STATUS(LC=0, data as string)
declare command &H84 &H04 FC_VAULT_OPEN(data as string)
declare command &H84 &H08 FC_VAULT_IMPORT(data as string)
declare command &H84 &H10 FC_VAULT_REENCRYPT(data as string)
declare command &H84 &H12 FC_VAULT_HMAC_SHA1(data as string)
declare command &H84 &H14 FC_VAULT_HMAC_SHA256(data as string)
declare command &H84 &H16 FC_VAULT_CLOSE(LC=0, data as string)
"""

from .error import CardIOError
import hmac
import hashlib


def HMAC_SHA256(key, data):
    return hmac.digest(key, data, hashlib.sha256)






class CardSession:

    def __init__(self):
        self.cardRequest = CardRequest(timeout=10) #, cardType=cardtype)

    def login(self, password):
        conn = self.cardService.connection
        password = hashlib.sha1(password).digest()
        
        auth_challenge = self.__run_command(FC_GET_CHALLENGE())

        session_key = HMAC_SHA256(password, auth_challenge)
        s_res = HMAC_SHA256(password, session_key)
        ret_ok = HMAC_SHA256(session_key, auth_challenge)

        self.__session_key = session_key

        verify_result = self.__run_command(FC_VERIFY(s_res))
        verified = (verify_result == ret_ok)

        if not verified:
            self.__session_key = None
        return verified

    def __run_command(self, cmd):
        if isinstance(cmd, EncryptedCardCommand):
            return cmd(self.cardService.connection, self.__session_key)
        else:
            return cmd(self.cardService.connection)


    def open_vault(self, vault_id, password):
        return self.__run_command(FC_VAULT_OPEN(vault_id, password))


    def __enter__(self, *args, **kvargs):
        self.cardService = self.cardRequest.waitforcard()

        self.cardService.connection.connect()
        atr = ATR(self.cardService.connection.getATR())
        identification = bytes(atr.getHistoricalBytes())

        #if identification != b"feder.cards/pg1":
        #    raise Exception("Wrong card inserted.")
        print(identification)

        return self
            

    def __exit__(self, *args, **kvargs):
        pass
