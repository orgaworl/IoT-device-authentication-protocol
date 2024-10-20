#import hashlib
from gmssl import *

class SM3HashComp:
    def Hash(self,data: any) -> int:
        """
        普通哈希函数
        :param data:
        :return:
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        sm3_hash = Sm3()
        sm3_hash.update(data)
        data_hash = sm3_hash.digest()
        data_hash = int(data_hash.hex(), 16)
        return data_hash


    def two_hashed_OPRF(self,key: int, data_1: str, data_2: int, p: int) -> str:
        """
        2hashed OPRF函数：OPRF(key, data_1, data_2, p) = Hash(data_1, (data_2)^key) mod p
        :param key: 指数
        :param data_1: 待哈希的值
        :param data_2: 哈希后的数据
        :param p: 群的阶数
        :return:
        """
        temp_data = pow(data_2, key, p)   # 临时的数据，data_2的key次方
        data = data_1 + str(temp_data)    # 字符串拼接
        data = data.encode('utf-8')
        sm3_hash = Sm3()
        sm3_hash.update(data)
        data_hash = sm3_hash.digest()
        res=bytearray(16)
        for i in range(16):
            res[i]=data_hash[i]^data_hash[i+16]
        assert(len(res),16)
        return res.hex()

