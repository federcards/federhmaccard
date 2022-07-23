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




class FederPRURI:

#    @static
#    def fromstring(self, uri):
#        pass

    def __init__(self, algorithm, seed, combinations):
        assert isinstance(algorithm, FederPRURIAlgorithm)
        assert isinstance(combinations, FederPRURICombinations)
        assert int(combinations.value) != 0
        assert type(seed) in [str, bytes]

        self.algorithm = algorithm
        self.combinations = combinations.value & 0x0F

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

    print(str(u))
