#!/usr/bin/env python3
from enum import Enum
from urllib.parse import urlparse, unquote_to_bytes, quote_from_bytes

SCHEME = "federpr"


class FederPRURIAlgorithm(Enum):
    SHA1 = 1
    SHA256 = 2
   
class FederPRURICombinations(Enum):
    UPPERCASE = 1
    LOWERCASE = 2
    NUMERICAL = 4
    SPECIAL   = 8


def parse_qs(string):
    ret = {}
    parts = string.split("&")
    for kv in parts:
        kvparts = kv.split("=")
        if len(kvparts) < 2: kvparts += [None,]
        k,v = kvparts[:2]
        ret[k] = v
    return ret



class FederPRURI:

    @staticmethod
    def fromstring(uri):
        parsed = urlparse(uri)
        if parsed.scheme != SCHEME:
            raise Exception("Not a valid FederPRURI.")

        qsparsed = parse_qs(parsed.query)
        print(qsparsed)

        algorithm = FederPRURIAlgorithm.SHA1
        if "algorithm" in qsparsed:
            if qsparsed["algorithm"] == "SHA256":
                algorithm = FederPRURIAlgorithm.SHA256
            elif qsparsed["algorithm"] != 'SHA1':
                raise Exception("Unsupported hash algorithm.")

        seed = b""
        if "seed" in qsparsed:
            seed = unquote_to_bytes(qsparsed["seed"])
        
        combinations = ( 
            FederPRURICombinations.UPPERCASE.value |
            FederPRURICombinations.LOWERCASE.value |
            FederPRURICombinations.NUMERICAL.value |
            FederPRURICombinations.SPECIAL.value )
            
        if "combinations" in qsparsed:
            combinations = int(qsparsed["combinations"][0])

        print("seed", seed)

        return FederPRURI(algorithm, seed, combinations)



    def __init__(self, algorithm, seed, combinations):
        assert isinstance(algorithm, FederPRURIAlgorithm)
        assert type(seed) in [str, bytes]
        if isinstance(combinations, FederPRURICombinations):
            combinations = combinations.value
        else:
            assert type(combinations) == int
        assert combinations != 0

        self.algorithm = algorithm
        self.combinations = combinations & 0x0F

        if type(seed) == bytes:
            self.seed = seed
        else:
            self.seed = seed.encode("ascii")

    def __str__(self):
        return "%s://?seed=%s&algorithm=%s&combinations=%d" % (
            SCHEME,
            quote_from_bytes(self.seed),
            self.algorithm.name,
            self.combinations
        )


if __name__ == "__main__":

    import os
    
    u = FederPRURI(
        algorithm=FederPRURIAlgorithm.SHA256,
        seed=os.urandom(32),
        combinations=FederPRURICombinations.UPPERCASE
    )

    u2 = FederPRURI.fromstring(str(u))
    print(str(u))
    print(str(u2))
