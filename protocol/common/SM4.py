
from gmssl import *
from Cryptodome.Util.Padding import pad, unpad


class SM4:
    def __init__(self):
        self.key_size = SM4_KEY_SIZE
        self.block_size = SM4_BLOCK_SIZE
        
    def PadKey(self, key: bytes) -> bytes:
        """
        待加密的密钥补齐到对应的位数
        :param key: 密钥
        :return: 补齐后的密钥
        """
        if len(key) > self.key_size:          # 如果密钥长度超过 AES_KEY_SIZE
            return key[:self.key_size]        # 截取前面部分作为密钥并返回
        while len(key) % self.key_size != 0:  # 不到 AES_KEY_SIZE 长度则补齐
            key += ' '.encode()               # 补齐的字符可用任意字符代替
        return key
    
    def EnCrypt(self,key:bytes,data:bytes)->bytes:
        key = self.PadKey(key)
        data=pad(data,self.block_size)
        
        sm4=Sm4(key,DO_ENCRYPT)
        res=bytes()
        for i in range(len(data)//self.block_size):
            res+=sm4.encrypt(data[self.block_size*i:self.block_size*(i+1)])
        return res
    
    
    def DeCrypt(self,key:bytes,data:bytes)->bytes:
        key = self.PadKey(key)
        sm4=Sm4(key,DO_DECRYPT)
        res=bytes()
        for i in range(len(data)//self.block_size):
            res+=sm4.encrypt(data[self.block_size*i:self.block_size*(i+1)])
        res=unpad(res,self.block_size)
        return res



# ---------------------------------------
