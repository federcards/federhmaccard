const MAIN_SECRET_INITIALIZED = &HF0
const MAIN_SECRET_DEFAULT_KEY = "default"

EEPROM __main_secret_encrypted as String
EEPROM __main_secret_initialized as byte = &H0F
PUBLIC __main_secret as string


function main_secret_do_hmac(byval hmacval as string) as string
    if __main_secret = "" then
        main_secret_do_hmac = "! requires unlock"
        exit function
    end if
    if Len(hmacval) < 5 then
        main_secret_do_hmac = "! HMAC arg too short"
        exit function
    end if
    main_secret_do_hmac = "OK," + HMAC_SHA1(__main_secret, hmacval)
end function


function main_secret_unlock(byval password as string) as string
    if __main_secret <> "" then
        main_secret_unlock = "OK"
        exit function
    end if
    if __main_secret_initialized <> MAIN_SECRET_INITIALIZED then
        main_secret_unlock = "! card uninitialized"
        exit function
    end if
    __main_secret = crypto_decrypt(password, __main_secret_encrypted)
    if __main_secret = "" then
        main_secret_unlock = "! unlock failed"
    else
        main_secret_unlock = "OK"
    end if
end function


function main_secret_import(byval secret as string) as string
    if __main_secret_initialized = MAIN_SECRET_INITIALIZED then
        if __main_secret = "" then
            main_secret_import = "! requires unlock"
            exit function
        end if
    end if
    __main_secret_encrypted = crypto_encrypt(MAIN_SECRET_DEFAULT_KEY, secret)
    __main_secret = secret
    main_secret_import = "OK"
end function


function main_secret_set_password(byval password as string) as string
    if __main_secret_initialized = MAIN_SECRET_INITIALIZED then
        if __main_secret = "" then
            main_secret_set_password = "! requires unlock"
            exit function
        end if
    else
        main_secret_set_password = "! card uninitialized"
        exit function
    end if
    __main_secret_encrypted = crypto_encrypt(password, __main_secret)
    main_secret_set_password = "OK"
end function

