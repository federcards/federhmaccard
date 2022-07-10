' HMACCARD source code
' --------------------
' The HMACCARD is a simple card for generating HMAC based passwords. It carries
' only one thing: the main secret. And it's saved in encrypted form on card.
'
' Once the main secret is decrypted, the card can be used. The user supplies an
' argument, and the card derives it's HMAC value based on that argument. The
' HMAC value is then returned to the outside world, and it can be encoded into
' a suitable password.
'
' Thus, HMACCARD is a low cost authentication device that provides the "what
' you possess". The main secret on card cannot be exported, and thus the card
' is a hard-to-be-copied device suitable for most daily use. The "seeds" for
' each password can be stored even in plaintext form, and even so it's not
' possible to hack the main secret based on some leaked passwords. This is a
' main advantage over centeralized password managers, which relies on a main
' passphrase, and once that is leaked, every password is compromised.
'
' To provide some redundancy, the main secret is imported rather than generated
' on-card. We assume the user will lock the main secret at least in a safe,
' just in case their cards get damaged, they can issue new cards for replace-
' ment.
'
' Also there is currently no encryption for APDU, not because we cannot
' implement one, but we trust the user will at least plug the card into a
' trustful computer running no keyloggers. Anyway, the derived passwords will
' be entered (most likely via clipboard) into other programs, and it won't help
' much if malware is running on computer. For sake of defensing in depth, we
' may implement one later.


Option Explicit

#Pragma CodeBlock "factory_init"

#include AES.DEF
#include SHA.DEF
#include Card.def

#include util.bas

#include lib/hmac.bas
#include lib/crypto.bas
#include lib/hashcash_guardian.bas

#include vault.bas
#include authentication.bas
#include factory.bas




EEPROM factory_init_done as Byte = 0
command &H88 &H88 FACTORY_INIT(LC=0, data as string)
    if 0 = factory_init_done then
        call do_factory_init()
        factory_init_done = &HAA
        erase "factory_init"
        data = "OK,initialized"
    end if
    data = "OK,nothing to do"
end command


command &H88 &H86 FC_FACTORY_RESET(data as string)
    data = authentication_factory_reset(data)
end command





command &H88 &H00 Greet(LC=0, data as string)
   'data="Federcard/HMACCARD"
   data = HMAC_SHA256("key", "The quick brown fox jumps over the lazy dog")
end command


command &H88 &H84 FC_GET_CHALLENGE(LC=0, data as string)
    data = authentication_get_challenge()
end command



command &H88 &H20 FC_VERIFY(data as string)
    dim verification_data as string*32
    verification_data = Left$(data, 32)
    data = authentication_verify(verification_data)
end command



command &H84 &H00 FC_STATUS(LC=0, data as string)
    data = authentication_encrypt_message(vault_status())
end command

command &H84 &H24 FC_CHANGE_PASSWORD(data as string)
    data = authentication_encrypt_message(_
        authentication_set_password(_
            authentication_decrypt_message(data)))
end command




command &H84 &H04 FC_VAULT_OPEN(data as string)
    data = authentication_decrypt_message(data)
    if data = "" then
        exit command
    end if
    data = vault_open(asc(data(1)), Mid$(data, 2))
    data = authentication_encrypt_message(data)
end command


command &H84 &H08 FC_VAULT_IMPORT(data as string)
    data = authentication_decrypt_message(data)
    if data = "" then
        exit command
    end if
    data = vault_import(asc(data(1)), Mid$(data, 2))
    data = authentication_encrypt_message(data)
end command


command &H84 &H10 FC_VAULT_REENCRYPT(data as string)
    data = authentication_decrypt_message(data)
    if data = "" then
        exit command
    end if
    data = vault_reencrypt(data)
    data = authentication_encrypt_message(data)
end command


command &H84 &H12 FC_VAULT_HMAC_SHA1(data as string)
    data = authentication_decrypt_message(data)
    if data = "" then
        exit command
    end if
    data = vault_hmac_sha1(data)
    data = authentication_encrypt_message(data)
end command


command &H84 &H14 FC_VAULT_HMAC_SHA256(data as string)
    data = authentication_decrypt_message(data)
    if data = "" then
        exit command
    end if
    data = vault_hmac_sha256(data)
    data = authentication_encrypt_message(data)
end command


command &H84 &H16 FC_VAULT_CLOSE(LC=0, data as string)
    call vault_close()
    data = authentication_encrypt_message("OK")
end command