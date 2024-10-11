import hashlib


def Hash(data: any) -> int:
    """
    普通哈希函数
    :param data:
    :return:
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    sha256_hash = hashlib.new('sha256')
    sha256_hash.update(data)
    data_hash = sha256_hash.hexdigest()  # 16进制字符串
    data_hash = int(data_hash, 16)
    return data_hash


def two_hashed_OPRF(key: int, data_1: str, data_2: int, p: int) -> str:
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
    sha256_hash = hashlib.new('sha256')
    sha256_hash.update(data)
    data_hash = sha256_hash.hexdigest()  # 16进制字符串
    return data_hash

