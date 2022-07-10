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
'      RET_OK = HMAC(SK, NONCE)
'  3. the user calls GET_CHALLENGE and gets NONCE. The user calculates its SK,
'     SRES_2 and RET_OK in the same way of above step accordingly.
'  4. the user calls VERIFY with argument(SRES_2). The card verifies 
'     SRES_2 == SRES_1. If yes, secure access is granted, and it returns
'     RET_OK.
'  5. the user verifies RET_OK to authenticate the card.


' Default password: "federcard"
const __authentication_default_password=Chr$(_
    236, 94, 211, 160, 224, 68, 16, 153, 105, 45, 152, 44, 138, 239, 157, 213, 183, 187, 241, 153)
    
EEPROM __authentication_password as string*60=_
    __authentication_default_password + _
    __authentication_default_password + _
    __authentication_default_password

public __authentication_initialized as Integer
public __authentication_verified as Integer

type authentication_session_state
    nonce as string*20
    session_key as string*20
    response as string*20
    ret_ok as string*20
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

    dim hashed_password as string*20
    hashed_password = ShaHash(plain_password)
    __authentication_password = hashed_password+hashed_password+hashed_password
    
    authentication_set_password = "OK"
end function

function authentication_get_password() as string*20
    authentication_get_password = resume_triplestr(__authentication_password, 20)
end function


sub authentication_reset_state()
    __authentication_verified = False

    dim authentication_password as string
    authentication_password = authentication_get_password()
    
    dim nonce as string*20
    nonce = crypto_random_bytes(20)
    __authentication_state.nonce = nonce
    
    dim sk as string*20
    sk = HMAC_SHA1(authentication_password, __authentication_state.nonce)
    __authentication_state.session_key = sk

    dim response as string*20
    response = HMAC_SHA1(authentication_password, sk)
    __authentication_state.response = response
    
    __authentication_state.ret_ok = HMAC_SHA1(sk, nonce)
        
    __authentication_initialized = True
end sub



function authentication_get_challenge() as string*20
    call authentication_reset_state()
    authentication_get_challenge = __authentication_state.nonce
end function


function authentication_verify(byval answer as string*20) as string
    if strcmp_n(answer, __authentication_state.response, 20) = True then
        __authentication_verified = True
        authentication_verify = __authentication_state.ret_ok
    else
        call authentication_reset_state()
        authentication_verify = "ERR"
    end if        
end function



