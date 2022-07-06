public hashcash_nonce as string*32

sub hashcash_init()
    hashcash_nonce = crypto_random32bytes()
end sub


function hashcash_validate(tested as string) as string
    dim result as string
    result = ShaHash(hashcash_nonce + tested)
    call hashcash_init()
    
    dim count as byte
    count = asc(result(1)) xor asc(result(2)) xor asc(result(3)) ' first 24 bits
    if count > 0 then
        hashcash_validate = ""
    else
        hashcash_validate = Mid$(tested, 8)
    end if
end function