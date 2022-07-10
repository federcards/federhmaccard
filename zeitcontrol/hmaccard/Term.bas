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



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
public menu_choice as byte
public vault_status as string

MENU:
call FC_STATUS(data$) : call CheckSW1SW2()
vault_status = crypto_decrypt(session_key, data$)

Cls
print "Menu of commands"
print "================"
if asc(vault_status(4)) = 0 then
    print "Currently no vault open."
else
    print "Current vault=", asc(vault_status(4))
end if

print "1. open vault"
print "2. import vault"
print "3. change vault password"
print "4. calculate HMAC-SHA1"
print "5. calculate HMAC-SHA256"
print "6. close vault"
print ""
print "Your choice?"


input menu_choice

if 1 = menu_choice then goto VAULT_OPEN
if 2 = menu_choice then goto VAULT_IMPORT
if 3 = menu_choice then goto VAULT_REENCRYPT
if 4 = menu_choice then goto VAULT_SHA1
if 5 = menu_choice then goto VAULT_SHA256
if 6 = menu_choice then goto VAULT_CLOSE

goto MENU

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
VAULT_OPEN:

dim vault_id as byte
dim vault_password as string
dim vault_opened as integer

print "Vault id:"
input vault_id
print "Vault password:"
input vault_password
print "Try open vault id=",vault_id
data$ = crypto_encrypt(session_key, chr$(vault_id) + vault_password)
call FC_VAULT_OPEN(data$) : call CheckSW1SW2()
data$ = crypto_decrypt(session_key, data$)
print(data$)

vault_opened = ("OK" = Left$(data$, 2))

input menu_choice : goto MENU

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
VAULT_IMPORT:

dim vault_secret as string
print "Vault id:"
input vault_id
print "Vault secret in plaintext:"
input vault_secret

print "Import to vault id=", vault_id
data$ = crypto_encrypt(session_key, chr$(vault_id) + vault_secret)
call FC_VAULT_IMPORT(data$) : call CheckSW1SW2()
data$ = crypto_decrypt(session_key, data$)
print(data$)
    
input menu_choice : goto MENU

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
VAULT_REENCRYPT:


print "Changing password for current vault. Your new password?"
dim newpassword as string
input newpassword

data$ = crypto_encrypt(session_key, newpassword)
call FC_VAULT_REENCRYPT(data$) : call CheckSW1SW2()
data$ = crypto_decrypt(session_key, data$)
print(data$)

input menu_choice : goto MENU

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
VAULT_SHA1:

print("Calculating HMAC-SHA1 for current vault. Your argument?")
input data$
data$ = crypto_encrypt(session_key, data$)
call FC_VAULT_HMAC_SHA1(data$) : call CheckSW1SW2()
data$ = crypto_decrypt(session_key, data$)
if Left$(data$, 3) = "OK," then
    print "success:", str2hex(Mid$(data$, 4))
else
    print data$
end if

input menu_choice : goto MENU

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
VAULT_SHA256:

print("Calculating HMAC-SHA256 for current vault. Your argument?")
input data$
data$ = crypto_encrypt(session_key, data$)
call FC_VAULT_HMAC_SHA256(data$) : call CheckSW1SW2()
data$ = crypto_decrypt(session_key, data$)
if Left$(data$, 3) = "OK," then
    print "success:", str2hex(Mid$(data$, 4))
else
    print data$
end if

input menu_choice : goto MENU

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
VAULT_CLOSE:

call FC_VAULT_CLOSE(data$) : call CheckSW1SW2()
data$ = crypto_decrypt(session_key, data$)
if data$ = "OK" then
    print "Vault closed."
else
    print "unknown error"
end if

input menu_choice : goto MENU

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
DONE:
print "Bye."
