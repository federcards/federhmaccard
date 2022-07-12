' A constant time strcmp function, comparing string up to 253 bytes.

PUBLIC __strcmp_253_a AS STRING*254
PUBLIC __strcmp_253_b AS STRING*254
CONST __zero_254 = Chr$(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

PUBLIC __strcmp_64_a AS STRING*65
PUBLIC __strcmp_64_b AS STRING*65




FUNCTION strcmp_253(a as STRING, b as STRING) as Integer
    __strcmp_253_a = a + "!"
    __strcmp_253_b = b + "!"

    PRIVATE m as BYTE = 0
    PRIVATE i as BYTE
    FOR i = 1 TO 254
        m = m OR (Asc(__strcmp_253_a(i)) XOR Asc(__strcmp_253_b(i)))
    NEXT
    
    strcmp_253 = (0 = m)
    
    __strcmp_253_a = __zero_254
    __strcmp_253_b = __zero_254

END FUNCTION


FUNCTION strcmp_n(a as STRING, b as STRING, n as BYTE) as Integer
    __strcmp_253_a = a + "!"
    __strcmp_253_b = b + "!"

    PRIVATE m as BYTE = 0
    PRIVATE i as BYTE
    FOR i = 1 TO n + 1
        m = m OR (Asc(__strcmp_253_a(i)) XOR Asc(__strcmp_253_b(i)))
    NEXT
    
    strcmp_n = (0 = m)
    
    __strcmp_253_a = __zero_254
    __strcmp_253_b = __zero_254

END FUNCTION


FUNCTION strcmp_64(a as STRING, b as STRING) as Integer
    __strcmp_64_a = a + "!"
    __strcmp_64_b = b + "!"

    PRIVATE m as BYTE = 0
    PRIVATE i as BYTE
    FOR i = 1 TO 65
        m = m OR (Asc(__strcmp_64_a(i)) XOR Asc(__strcmp_64_b(i)))
    NEXT
    
    strcmp_64 = (0 = m)
    
    __strcmp_64_a = Left$(__zero_254, 64)
    __strcmp_64_b = __strcmp_64_a

END FUNCTION


FUNCTION resume_triplestr(s as STRING, length as BYTE) as STRING
    PRIVATE i as BYTE
    PRIVATE j as BYTE
    PRIVATE k as BYTE
    PRIVATE result as STRING*84
    IF length > 84 THEN
        resume_triplestr = ""
        EXIT FUNCTION
    END IF
    j = length
    k = length * 2
    FOR i = 1 to length
        j = j + 1
        k = k + 1
        result(i) = chr$((asc(s(i)) OR asc(s(j))) AND (asc(s(i)) OR asc(s(k))) AND (asc(s(j)) OR asc(s(k))))
    NEXT
    resume_triplestr = Left$(result, length)
END FUNCTION


FUNCTION resume_triplestr3(s1 as STRING, s2 as STRING, s3 as STRING, length as BYTE) as STRING
    PRIVATE i as BYTE
    PRIVATE result as STRING*120
    IF length > 120 THEN
        resume_triplestr3 = ""
        EXIT FUNCTION
    END IF
    
    FOR i = 1 to length
        result(i) = chr$((asc(s1(i)) OR asc(s2(i))) AND (asc(s1(i)) OR asc(s3(i))) AND (asc(s2(i)) OR asc(s3(i))))
    NEXT
    resume_triplestr3 = Left$(result, length)
END FUNCTION