' Authentication and security state changer.
'
' This module provides the access control function for this card:
'  1. A password has to be set before using this card. It's stored on the card
'     in plaintext.
'  2. The GET_CHALLENGE() function is exposed as command, and returns to the
'     outside world a nonce, that is changed after each VERIFY call, and must
'     be used during authentication.
'  3. The VERIFY() function call is used to change the card state to 
'     "authenticated". If verification failed, it returns "ERR". Otherwise, it
'     returns Hash(NONCE+SK), where SK is the established session key and nonce
'     the previously used nonce.
'
' Authentication algorithm:
'  0. the card stores user supplied password in form AP=SHA1(password).
'  1. the card generates a random NONCE
'  2. from NONCE, the card generates:   // denoting HMAC=HMAC(secret, input)
'      SK = HMAC(AP, NONCE) // AP=SHA1(password) is previously stored in E2PROM
'      SRES_1 = HMAC(AP, SK)
'      SRES_FACTORY_RESET = SHA256(NONCE)
'      RET_OK = HMAC(SK, NONCE)
'  3. the user calls GET_CHALLENGE and gets NONCE. The user calculates its SK,
'     SRES_2 and RET_OK in the same way of above step accordingly.
'  4. the user calls VERIFY with argument(SRES_2). The card verifies 
'     SRES_2 == SRES_1. If yes, secure access is granted, and it returns
'     RET_OK.
'  5. the user verifies RET_OK to authenticate the card.


const AUTHENTICATION_TOKEN_SIZE = 32
const AUTHENTICATION_SECRET_SIZE = 20


' Default password: "federcard"
const __authentication_default_password=Chr$(_
    236, 94, 211, 160, 224, 68, 16, 153, 105, 45, 152, 44, 138, 239, 157, 213, 183, 187, 241, 153)
    
EEPROM __authentication_password as string*(3*AUTHENTICATION_SECRET_SIZE)=_
    __authentication_default_password + _
    __authentication_default_password + _
    __authentication_default_password

public __authentication_initialized as Integer
public __authentication_verified as Integer
public authentication_write_enabled as Integer

type authentication_session_state
    nonce as string*AUTHENTICATION_TOKEN_SIZE
    session_key as string*AUTHENTICATION_TOKEN_SIZE
    response as string*AUTHENTICATION_TOKEN_SIZE
    response_factory_reset as string*AUTHENTICATION_TOKEN_SIZE
    ret_ok as string*AUTHENTICATION_TOKEN_SIZE
end type

public __authentication_state as authentication_session_state



function authentication_verified() as Integer
    authentication_verified = (_
        __authentication_verified = True _
        and __authentication_initialized = True)
end function



function authentication_set_password(plain_password as string) as string
    if authentication_verified() = 0 then
        authentication_set_password = "ERR"
        exit function
    end if

    dim hashed_password as string*AUTHENTICATION_SECRET_SIZE
    hashed_password = ShaHash(plain_password)
    __authentication_password = hashed_password+hashed_password+hashed_password
    
    authentication_set_password = "OK"
end function

function authentication_get_password() as string*AUTHENTICATION_SECRET_SIZE
    authentication_get_password = resume_triplestr(__authentication_password, AUTHENTICATION_SECRET_SIZE)
end function


sub authentication_reset_state()
    __authentication_verified = False
	authentication_write_enabled = False

    dim authentication_password as string
    authentication_password = authentication_get_password()
    
    __authentication_state.nonce = crypto_random_bytes(AUTHENTICATION_TOKEN_SIZE)
    __authentication_state.response_factory_reset = Sha256Hash(__authentication_state.nonce)
    
    __authentication_state.session_key = HMAC_SHA256(authentication_password, __authentication_state.nonce)

    'dim response as string*AUTHENTICATION_TOKEN_SIZE
    'response = HMAC_SHA256(authentication_password, sk)
    __authentication_state.response = HMAC_SHA256(authentication_password, __authentication_state.session_key)
    
    __authentication_state.ret_ok = HMAC_SHA256(__authentication_state.session_key, __authentication_state.nonce)
        
    __authentication_initialized = True
end sub



function authentication_get_challenge() as string*AUTHENTICATION_TOKEN_SIZE
    call authentication_reset_state()
    authentication_get_challenge = __authentication_state.nonce
end function


function authentication_verify(byval answer as string*AUTHENTICATION_TOKEN_SIZE) as string
    if strcmp_n(answer, __authentication_state.response, AUTHENTICATION_TOKEN_SIZE) = True then
        __authentication_verified = True
        authentication_verify = __authentication_state.ret_ok
    else
        call authentication_reset_state()
        authentication_verify = "ERR"
    end if        
end function


function authentication_write_enable() as string
	if authentication_verified() = False then
		authentication_write_enable = "ERR"
		exit function
	end if
	authentication_write_enabled = True
	authentication_write_enable = "OK"
end function


function authentication_encrypt_message(message as string) as string
    if authentication_verified() = False then
        authentication_encrypt_message = ""
        exit function
    end if
    authentication_encrypt_message = crypto_encrypt(_
        __authentication_state.session_key, message)
end function


function authentication_decrypt_message(message as string) as string
    if authentication_verified() = False then
        authentication_decrypt_message = ""
        exit function
    end if
    authentication_decrypt_message = crypto_decrypt(_
        __authentication_state.session_key, message)
end function


'function authentication_factory_reset(checksum as string) as string
' ... -> see factory.bas