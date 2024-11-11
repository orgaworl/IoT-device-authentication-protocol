from ecpy import curves


class Curve:

    def __init__(self,curve_name:str='Ed25519'):
        """
        默认 Ed25519 曲线类
        """

        # 选择曲线
        self.curve_name=curve_name
        self.curve = curves.Curve.get_curve(curve_name)
        # 获取曲线的阶和生成元的点
        self.order = self.curve.order
        self.generator_point = self.curve.generator



    def to_bytes(self, point):
        """
        点的序列化
        :param point: Ed25519曲线的点
        :return:点的字节化表示
        """
        point_bytes = self.curve.encode_point(point)
        if type(point_bytes)==list:
            point_bytes=bytes(point_bytes)
        
        return point_bytes

    def from_bytes(self, point_bytes):
        """
        点的反序列化
        :param point_bytes: 点的字节化表示
        :return:Ed2551曲线的点
        """
        point = self.curve.decode_point(point_bytes)
        return point    
    def add(self, Q, P):
        """
        点的加法
        :param Q: 点
        :param P: 点
        :return:
        """
        return Q + P

    def sub(self, Q, P):
        """
        点的减法
        :param Q: 点
        :param P: 点
        :return:
        """
        return Q - P

    def mul(self, scale, P):
        """
        点的数乘
        :param scale: 数
        :param P: 点
        :return:
        """
        return scale * P