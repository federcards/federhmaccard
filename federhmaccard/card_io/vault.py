#!/usr/bin/env python3

from .commands.FC_VAULT_OPEN        import *
from .commands.FC_VAULT_STATUS      import *
from .commands.FC_VAULT_IMPORT      import *
from .commands.FC_VAULT_REENCRYPT   import *
from .commands.FC_VAULT_HMAC_SHA1   import *
from .commands.FC_VAULT_HMAC_SHA256 import *
from .commands.FC_VAULT_CLOSE       import *


class VaultAccess:

    def __init__(self, card_session, vault_id):
        self.session = card_session
        self.vault_id = vault_id

    def __enter__(self, *args, **kvargs):
        return self

    def __exit__(self, *args, **kvargs):
        print(self.session.run_command(FC_VAULT_CLOSE()))

    def open(self, password):
        print(self.session.run_command(FC_VAULT_OPEN(self.vault_id, password)))
