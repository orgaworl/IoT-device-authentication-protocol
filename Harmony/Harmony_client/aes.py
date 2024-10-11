from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad


class Aes:
    """
    AES_BLOCK_SIZE = AES.block_size  # AES 加密数据块大小, 只能是16
    AES_KEY_SIZE = 16  # AES 密钥长度（单位字节），可选 16、24、32，对应 128、192、256 位密钥
    """

    def __init__(self, AES_KEY_SIZE=16, AES_BLOCK_SIZE=AES.block_size):  # 初始化类的属性
        self.key_size = AES_KEY_SIZE
        self.block_size = AES_BLOCK_SIZE

    def PadKey(self, key: bytes) -> bytes:
        """
        待加密的密钥补齐到对应的位数
        :param key: 密钥
        :return: 补齐后的密钥
        """
        if len(key) > self.key_size:          # 如果密钥长度超过 AES_KEY_SIZE
            return key[:self.key_size]        # 截取前面部分作为密钥并返回
        while len(key) % self.key_size != 0:  # 不到 AES_KEY_SIZE 长度则补齐
            key += ' '.encode()              # 补齐的字符可用任意字符代替
        return key                           # 返回补齐后的密钥

    def EnCrypt(self, key: bytes, message: bytes) -> bytes:
        """
        AES加密算法
        :param key: 加密密钥
        :param message: 待加密明文
        :return:
        """
        key = self.PadKey(key)                                         # 补齐密钥
        myCipher = AES.new(key, AES.MODE_ECB)                          # 新建一个 AES 算法实例，使用 ECB（电子密码本）模式
        encryptData = myCipher.encrypt(pad(message, self.block_size))  # 调用加密方法，得到加密后的数据
        return encryptData                                             # 返回加密数据

    def DeCrypt(self, key: bytes, encryptData: bytes) -> bytes:
        """
        AES解密算法
        :param key: 解密密钥
        :param encryptData: 待解密密文
        :return:
        """
        key = self.PadKey(key)                                           # 补齐密钥
        myCipher = AES.new(key, AES.MODE_ECB)                            # 新建一个 AES 算法实例，使用 ECB（电子密码本）模式
        message = unpad(myCipher.decrypt(encryptData), self.block_size)  # 调用解密方法，得到解密后的数据
        return message                                                   # 返回解密数据

