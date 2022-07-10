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


#include AES.DEF
#include SHA.DEF

#include util.bas

#include lib/hmac.bas
#include lib/crypto.bas
#include lib/hashcash_guardian.bas

#include main_secret.bas
#include authentication.bas

#include Card.def



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



command &H84 &H00 FC_ECHOTEST(data as string)
    data = authentication_encrypt_message(_
        "echoed:" + authentication_decrypt_message(data))
end command

command &H84 &H24 FC_CHANGE_PASSWORD(data as string)
    data = authentication_encrypt_message(_
        authentication_set_password(_
            authentication_decrypt_message(data)))
end command


command &H88 &H04 CardImport(LC=0, data as string)
    data = main_secret_import(data)
end command

command &H88 &H06 CardSetPassword(LC=0, data as string)
    data = main_secret_set_password(data)
end command

command &H88 &H08 HMAC(LC=0, data as string)
    data = main_secret_do_hmac(data)
end command