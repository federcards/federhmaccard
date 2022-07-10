Rem BasicCard Sample Source Code Template
Rem ------------------------------------------------------------------
Rem Copyright (C) 2008 ZeitControl GmbH
Rem You have a royalty-free right to use, modify, reproduce and 
Rem distribute the Sample Application Files (and/or any modified 
Rem version) in any way you find useful, provided that you agree 
Rem that ZeitControl GmbH has no warranty, obligations or liability
Rem for any Sample Application Files.
Rem ------------------------------------------------------------------
Option Explicit

#include Card.def
#Include COMMANDS.DEF
#Include COMMERR.DEF
#include MISC.DEF
#Include CARDUTIL.DEF


#include AES.DEF
#include SHA.DEF

#include util.bas

#include lib/hmac.bas
#include lib/crypto.bas


const HEX_ALPHABET = "0123456789ABCDEF"

function str2hex(ByVal strInput as String) as String
    private i as integer
    private c as byte
    for i = 1 to len(strInput)
        c = asc(strInput(i))
        Str2Hex = Str2Hex + HEX_ALPHABET(1+(c/16)) + HEX_ALPHABET(1+(c mod 16))
    next
end function







'  Execution starts here

' Wait for a card
Call WaitForCard()
' Reset the card and check status code SW1SW2
ResetCard : Call CheckSW1SW2()

' Test Hello World command
' A String variable to hold the response
Public Data$

Call FACTORY_INIT(Data$) : Call CheckSW1SW2()
print(Data$)
' Call the command and check the status
Call Greet(Data$) : Call CheckSW1SW2()
' Output the result
print str2hex(Data$)



Public auth_challenge as string
call FC_GET_CHALLENGE(auth_challenge) : Call CheckSW1SW2()
print "Challenge nonce acquired:", str2hex(auth_challenge)


public userpassword as string
print "Input password:"
'input userpassword
userpassword = "federcard"

userpassword = ShaHash(userpassword) ' Important
print "userpassword", str2hex(userpassword)


public session_key as string 
session_key = HMAC_SHA256(userpassword, auth_challenge)
public response as string 
response = HMAC_SHA256(userpassword, session_key)
public ret_ok as string
ret_ok = HMAC_SHA256(session_key, auth_challenge)

print "response", str2hex(response)
Data$ = response


call FC_VERIFY(Data$) : call CheckSW1SW2()

print str2hex(Data$)

if data$ <> ret_ok then
   print "Auth failed"
   goto DONE
end if


print "Auth passed. Session key ok."

'print "Echo test"

'print "input test string"
'input data$
'data$ = crypto_encrypt(session_key, data$)
'call FC_ECHOTEST(data$) : call CheckSW1SW2()
'print "we get", crypto_decrypt(session_key, data$)




print "Try open vault #2"
data$ = crypto_encrypt(session_key, chr$(2) + "password")
call FC_VAULT_OPEN(data$) : call CheckSW1SW2()
data$ = crypto_decrypt(session_key, data$)
print(data$)

dim vault_opened as integer


if left$(data$, 3) = "ERR" then
    print("Import vault #2 with a secret")
    data$ = crypto_encrypt(session_key, chr$(2) + "secret")
    call FC_VAULT_IMPORT(data$) : call CheckSW1SW2()
    data$ = crypto_decrypt(session_key, data$)
    print(data$)
    
    vault_opened = ("OK" = Left$(data$, 2))
else 
    vault_opened = True
end if


if not vault_opened then
    print "failed to open vault using given password."
    goto DONE
end if

print("Test SHA1")

data$ = crypto_encrypt(session_key, "test")
call FC_VAULT_HMAC_SHA1(data$) : call CheckSW1SW2()
data$ = crypto_decrypt(session_key, data$)
print str2hex(Mid$(data$, 4))

print("Test SHA256")

data$ = crypto_encrypt(session_key, "test")
call FC_VAULT_HMAC_SHA256(data$) : call CheckSW1SW2()
data$ = crypto_decrypt(session_key, data$)
print str2hex(Mid$(data$, 4))




DONE:
print "Done"
