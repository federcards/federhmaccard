from ._prototype import EncryptedCardCommand

class FC_VAULT_HMAC_SHA256(EncryptedCardCommand):

    def __init__(self, vault_id, message):
        assert type(message) == bytes
        EncryptedCardCommand.__init__(self, 0x84, 0x14)
        self.__data = bytes([vault_id]) + message 

    def build_request(self):
        return self.__data 

    def parse_response(self, sw1, sw2, response):
        return response