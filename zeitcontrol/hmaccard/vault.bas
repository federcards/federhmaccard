const VAULT_INITIALIZED = &HF0
const VAULT_DEFAULT_PASSWORD = "password"
const VAULT_ENCRYPTED_MAX_SIZE = 112
const VAULT_PLAIN_MAX_SIZE = VAULT_ENCRYPTED_MAX_SIZE - CRYPTO_OVERHEAD
const VAULTS_COUNT = 72


EEPROM __vault_protection_key as string*(32*3)

EEPROM __vaults_encrypted_1(1 to VAULTS_COUNT) as string*192
EEPROM __vaults_encrypted_2(1 to VAULTS_COUNT) as string*192
EEPROM __vaults_encrypted_3(1 to VAULTS_COUNT) as string*192

PUBLIC __vault_protection_key_ram as string
PUBLIC __vault_current_id as Byte
PUBLIC __vault_current_secret as String


function __vault_key_from_password(password as string) as string
    if __vault_protection_key_ram = "" then
        __vault_protection_key_ram = resume_triplestr(_
            __vault_protection_key, 32)
    end if
    __vault_key_from_password = HMAC_SHA256(_
        __vault_protection_key_ram, password)
end function


function __vault_read_encrypted(vault_id as byte) as string
    private vault_encrypted as string
    private vault_size as byte
    
    vault_encrypted = resume_triplestr3(_
        __vaults_encrypted_1(vault_id),_ 
        __vaults_encrypted_2(vault_id),_
        __vaults_encrypted_3(vault_id),_
        VAULT_ENCRYPTED_MAX_SIZE+1)
    vault_size = asc(vault_encrypted(1))
    if vault_size > VAULT_ENCRYPTED_MAX_SIZE then
        vault_size = VAULT_ENCRYPTED_MAX_SIZE
    end if
    __vault_read_encrypted = Mid$(vault_encrypted, 2, vault_size)
end function


sub __vault_write_encrypted(byval vault_id as byte, byval data as string)
    data = chr$(Len(data)) + data
    __vaults_encrypted_1(vault_id) = data
    __vaults_encrypted_2(vault_id) = data
    __vaults_encrypted_3(vault_id) = data    
end sub


function vault_open(byval vault_id as byte, byval password as string) as string
    private vault_key as string
    private vault_encrypted as string
    
    vault_id = ((vault_id - 1) mod VAULTS_COUNT) + 1
    vault_key = __vault_key_from_password(password)
    vault_encrypted = __vault_read_encrypted(vault_id)
    
    __vault_current_secret = crypto_decrypt(vault_key, vault_encrypted)
    if __vault_current_secret = "" then
        __vault_current_id = 0
        vault_open = "ERR,vault empty or wrong password"
    else
        __vault_current_id = vault_id
        vault_open = "OK"
    end if
end function


function vault_import(byval vault_id as byte, byval secret as string) as string
    if len(secret) > VAULT_PLAIN_MAX_SIZE then
        vault_import = "ERR,too long"
        exit function
    end if
    private vault_key as string
    vault_key = __vault_key_from_password(VAULT_DEFAULT_PASSWORD)
    call __vault_write_encrypted(vault_id, crypto_encrypt(vault_key, secret))
    
    __vault_current_id = vault_id
    __vault_current_secret = secret
    vault_import = "OK"
end function


function vault_reencrypt(byval newpassword as string) as string
    if 0 = __vault_current_id then
        vault_reencrypt = "ERR,no opened vault"
        exit function
    end if

    private vault_key as string
    vault_key = __vault_key_from_password(newpassword)
    call __vault_write_encrypted(_
        __vault_current_id, crypto_encrypt(vault_key, __vault_current_secret))
    vault_reencrypt = "OK"
end function


function vault_hmac_sha1(byval hmacval as string) as string
    if 0 = __vault_current_id then
        vault_hmac_sha1 = "ERR,no opened vault"
        exit function
    end if
    vault_hmac_sha1 = "OK," + HMAC_SHA1(__vault_current_secret, hmacval)
end function


function vault_hmac_sha256(byval hmacval as string) as string
    if 0 = __vault_current_id then
        vault_hmac_sha256 = "ERR,no opened vault"
        exit function
    end if
    vault_hmac_sha256 = "OK," + HMAC_SHA256(__vault_current_secret, hmacval)
end function


sub vault_close()
    __vault_current_id = 0
    __vault_current_secret = ""
end sub


function vault_status() as string
    vault_status = "OK," + chr$(__vault_current_id)
end function
