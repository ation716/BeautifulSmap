class QuadTreeNode:
    def __init__(self, boundary, capacity):
        # boundary 是当前节点的边界 (x_min, y_min, x_max, y_max)
        self.boundary = boundary
        self.capacity = capacity  # 当前节点的最大物体容量
        self.objects = []  # 存储在该节点中的物体
        self.divided = False  # 标记当前节点是否已经分裂
        self.nw = self.ne = self.sw = self.se = None  # 四个子节点

    def subdivide(self):
        """ 将当前节点分割成四个子节点 """
        x_min, y_min, x_max, y_max = self.boundary
        mid_x = (x_min + x_max) / 2
        mid_y = (y_min + y_max) / 2

        # 创建四个子节点
        nw_boundary = (x_min, y_min, mid_x, mid_y)
        self.nw = QuadTreeNode(nw_boundary, self.capacity)

        ne_boundary = (mid_x, y_min, x_max, mid_y)
        self.ne = QuadTreeNode(ne_boundary, self.capacity)

        sw_boundary = (x_min, mid_y, mid_x, y_max)
        self.sw = QuadTreeNode(sw_boundary, self.capacity)

        se_boundary = (mid_x, mid_y, x_max, y_max)
        self.se = QuadTreeNode(se_boundary, self.capacity)

        self.divided = True

    def insert(self, obj):
        """ 插入一个物体到当前节点 """
        # 检查物体是否在当前节点的边界内
        x, y = obj
        x_min, y_min, x_max, y_max = self.boundary
        if not (x_min <= x < x_max and y_min <= y < y_max):
            return False

        # 如果当前节点没有分裂且能容纳更多物体，直接插入
        if len(self.objects) < self.capacity:
            self.objects.append(obj)
            return True

        # 如果当前节点已经分裂，则将物体插入到相应的子节点中
        if not self.divided:
            self.subdivide()

        # 尝试将物体插入到各个子节点中
        if self.nw.insert(obj):
            return True
        elif self.ne.insert(obj):
            return True
        elif self.sw.insert(obj):
            return True
        elif self.se.insert(obj):
            return True

        return False


def query_range(node, range_boundary):
    # 如果当前节点的边界与查询范围没有交集，则返回空
    x_min, y_min, x_max, y_max = node.boundary
    rx_min, ry_min, rx_max, ry_max = range_boundary
    if x_max < rx_min or x_min > rx_max or y_max < ry_min or y_min > ry_max:
        return []

    # 如果当前节点的边界完全包含在查询范围内，直接返回当前节点的物体
    result = []
    if rx_min <= x_min and rx_max >= x_max and ry_min <= y_min and ry_max >= y_max:
        result.extend(node.objects)

    # 如果当前节点有子节点，递归查询子节点
    if node.divided:
        result.extend(query_range(node.nw, range_boundary))
        result.extend(query_range(node.ne, range_boundary))
        result.extend(query_range(node.sw, range_boundary))
        result.extend(query_range(node.se, range_boundary))

    return result


if __name__ == '__main__':
    pass