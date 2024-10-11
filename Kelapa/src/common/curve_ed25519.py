from ecpy import curves


class Curve:
    """
    Ed25519曲线类
    """
    # 选择曲线
    curve = curves.Curve.get_curve('Ed25519')
    # 获取曲线的阶和生成元的点
    order = curve.order
    generator_point = curve.generator

    def to_bytes(self, point):
        """
        点的序列化
        :param point: Ed25519曲线的点
        :return:点的字节化表示
        """
        point_bytes = self.curve.encode_point(point)
        return point_bytes

    def from_bytes(self, point_bytes):
        """
        点的反序列化
        :param point_bytes: 点的字节化表示
        :return:Ed2551曲线的点
        """
        point = self.curve.decode_point(point_bytes)
        return point
