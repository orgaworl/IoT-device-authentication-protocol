import random
import math


def generate_prime(n: int) -> int:
    """
    产生数 r, r 与 n-1 互素
    :param n: 素数，群的阶
    :return:
    """
    while True:
        r = random.randint(2, n - 1)
        if math.gcd(r, n-1) == 1:
            return r
