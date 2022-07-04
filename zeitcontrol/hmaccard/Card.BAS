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

#include Card.def


'#include AES.DEF
#include lib/hmac.bas
'#include lib/crypto.bas



EEPROM main_secret_encrypted as String

' This command just returns "Hello World" in response
' Since no input data is required, LC is set to 0
Command &H88 &H00 HelloWorld(LC=0, Data as String)
   Data="Hello World"
End Command

' This command saves Data in EEPROM.
' Since no output data is required, LE is disabled
Command &H88 &H02 WriteData(Data as String, Disable LE)
   ' Just copy it to EEPROM variable to save it
   CardData=Data
End Command

' This command reads data written by WriteData and 
' returns this data in response.
' Since no input data is required, LC is set to 0
Command &H88 &H04 ReadData(LC=0, Data as String)
   Data=CardData
End Command