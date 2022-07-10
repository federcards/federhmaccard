sub do_factory_reset()
    dim newkey as string
    newkey = crypto_random32bytes()
    __vault_protection_key = newkey+newkey+newkey
    __vault_protection_key_ram = ""
end sub


sub "factory_init" do_factory_init()
    dim newkey as string
    newkey = crypto_random32bytes()
    __vault_protection_key = newkey+newkey+newkey
    __vault_protection_key_ram = ""
end sub


function authentication_factory_reset(checksum as string) as string
    if __authentication_initialized = False then
        authentication_factory_reset = "ERR,get challenge first"
        exit function
    end if
    if checksum <> __authentication_state.response_factory_reset then
        authentication_factory_reset = "ERR,checksum invalid"
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







