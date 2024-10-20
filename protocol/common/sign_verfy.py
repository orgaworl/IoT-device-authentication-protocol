from ecpy import curves
from ecpy.keys import ECPublicKey, ECPrivateKey
from ecpy.ecdsa import ECDSA

# 选择曲线
curve = curves.Curve.get_curve('Ed25519')

# 获取曲线的阶和生成元的点
order = curve.order
generator_point = curve.generator


# 绑定私钥
def gen_private_key(priveta_key):
    private_key = ECPrivateKey(priveta_key, curve)
    return private_key


# 绑定公钥
def gen_public_key(public_key_point):
    public_key = ECPublicKey(public_key_point)
    return public_key


# 创建 ECDSA 对象
ecdsa = ECDSA()


# 签名算法
def sign(message, private_key):
    # 签名消息
    signature = ecdsa.sign(message, private_key)
    return signature


# 验证签名
def verify(message, signature, public_key):
    is_valid = ecdsa.verify(message, signature, public_key)
    if(is_valid):
        return True
    return False
