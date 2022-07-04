const CRYPTO_HMAC_LENGTH = 10       ' MUST BE LESS THAN 64
const CRYPTO_IV_LENGTH = 15
const CRYPTO_OVERHEAD = CRYPTO_HMAC_LENGTH + CRYPTO_IV_LENGTH



PUBLIC __CRYPTO_RANDOM_POOL as STRING*64


function crypto_random32bytes() as string
    private i as byte
    private r as Long
    for i=33 to 64 step 4
        r = Rnd
        Mid$(__CRYPTO_RANDOM_POOL, i, 4) = (r as String*4)
    next
    Left$(__CRYPTO_RANDOM_POOL, 32) = Sha256Hash(__CRYPTO_RANDOM_POOL)
    crypto_random32bytes = Left$(__CRYPTO_RANDOM_POOL, 32)
end function


function crypto_random_bytes(length as byte) as String
    private i as byte
    
    for i=0 to length / 32
        crypto_random_bytes = crypto_random_bytes + crypto_random32bytes()
    next
    crypto_random_bytes = Left$(crypto_random_bytes, length)
end function



sub xor_block(byref working_block as string, byref with_block as string)
    ' len(with_block) <= len(working_block)
    private i as byte
    for i = 1 to len(with_block)
        working_block(i) = chr$( asc(working_block(i)) xor asc(with_block(i)) )
    next
    
end sub


sub crypto_ctr(byref k as string, byval iv as string, byref message as string)
    private i_block as string*16
    private o_block as string*16
    private i as byte
    i_block = Left$(iv, CRYPTO_IV_LENGTH)
    
    i_block(16) = chr$(0)
    for i=1 to len(message) step 16
        o_block = AES(256, k, i_block)
        call xor_block(o_block, Mid$(message, i, 16))
        Mid$(message, i, 16) = o_block
        i_block(16) = chr$(asc(i_block(16)) + 1)
    next
end sub


function crypto_encrypt(byref encrypt_key as string, byval message as string) as string
    private iv as string
    private tag as string
    iv = Left$(crypto_random32bytes(), CRYPTO_IV_LENGTH)
    tag = Left$(HMAC_SHA1(encrypt_key, message), CRYPTO_HMAC_LENGTH)
    call crypto_ctr(encrypt_key, iv, message)
    
    crypto_encrypt = iv + tag + message
end function


function crypto_decrypt(byref decrypt_key as string, byval message as string) as string
    private iv as string
    private tag as string
    iv = Left$(message, CRYPTO_IV_LENGTH)
    tag = Mid$(message, CRYPTO_IV_LENGTH+1, CRYPTO_HMAC_LENGTH)
    message = Mid$(message, CRYPTO_IV_LENGTH + CRYPTO_HMAC_LENGTH + 1)
    call crypto_ctr(decrypt_key, iv, message)
    if strcmp_64(Left$(HMAC_SHA1(decrypt_key, message), CRYPTO_HMAC_LENGTH), tag) = 0 then
        crypto_decrypt = ""
        exit function
    end if
    crypto_decrypt = message
end function
