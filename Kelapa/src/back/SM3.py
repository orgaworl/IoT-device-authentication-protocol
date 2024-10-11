
from gmssl import *

class SM3:
    def hash(data:bytes)->bytes:   
        sm3 = Sm3()
        sm3.update(data)
        dgst = sm3.digest()
        return dgst
    