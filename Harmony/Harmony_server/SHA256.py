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

