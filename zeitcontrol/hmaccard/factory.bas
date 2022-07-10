sub do_factory_reset()
    __vault_protection_key = crypto_random32bytes()
end sub


function do_factory_init()
    __vault_protection_key = crypto_random32bytes()
end function


function authentication_factory_reset(checksum as string) as string
    if __authentication_initialized = False then
        authentication_factory_reset = "ERR"
        exit function
    end if
    call do_factory_reset()
    __authentication_password =_
        __authentication_default_password + _
        __authentication_default_password + _
        __authentication_default_password
    call authentication_reset_state()
    authentication_factory_reset = "OK"
end function







