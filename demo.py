import json
import os
import json
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 假设你的 JSON 数据已经读取并存入变量 data
# data = ...

# 获取点和线的数据
def smooth_curve(start_pos, end_pos, z_start, z_end):
    """ 使用三次样条插值生成平滑的曲线 """
    # X, Y, Z 坐标
    x_vals = [start_pos["x"], end_pos["x"]]
    y_vals = [start_pos["y"], end_pos["y"]]
    z_vals = [z_start, z_end]

    # 创建三次样条插值
    cs = CubicSpline([0, 1], np.array([x_vals, y_vals, z_vals]).T)

    # 生成平滑曲线的中间点
    t_vals = np.linspace(0, 1, 100)  # 生成100个点
    smoothed_points = cs(t_vals)

    return smoothed_points

# path=r"D:\workshop\scene\map_test\DLX_1_1.smap"
path=r"C:\Users\seer\Desktop\XLX_12-22.smap"
print(os.path.exists(path))
# def read_all():
#     # a=json.load('test.smap')
#     try:
#         with open(path, 'r',encoding='utf-8') as f:
#             for line in f:
#                 print(line)
#                 break
#             # a = json.loads(f)
#             # print(a)
#             pass
#     except Exception as e:
#         print(e)

# file_path = 'data.smap'

with open(path, 'rb') as file:
    data=json.load(file)
    # 获取点位列表
    points = data["advancedPointList"]

    # 创建一个字典来存储每个点的度数
    degree_dict = {point["instanceName"]: 0 for point in points}

    # 遍历线路，计算每个点的度数
    for curve in data["advancedCurveList"]:
        start_point = curve["startPos"]["instanceName"]
        end_point = curve["endPos"]["instanceName"]

        # 每条线路连接了两个点，因此两个点的度数都增加1
        degree_dict[start_point] += 1
        degree_dict[end_point] += 1

    # 创建3D图形
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 存储点的坐标和度数
    x_vals = []
    y_vals = []
    z_vals = []

    # 存储点坐标和度数
    for point in points:
        x = point["pos"]["x"]
        y = point["pos"]["y"]
        degree = degree_dict[point["instanceName"]]
        z = degree  # 这里z轴是度数
        x_vals.append(x)
        y_vals.append(y)
        z_vals.append(z)

    # 绘制三维散点图
    ax.scatter(x_vals, y_vals, z_vals, c=z_vals, cmap='viridis', s=50)
    # projection_x_vals = x_vals
    # projection_y_vals = y_vals
    # projection_z_vals = [0] * len(x_vals)  # 将z设置为0
    # ax.scatter(projection_x_vals, projection_y_vals, projection_z_vals, c='r', marker='x', s=30, label='Projection')

    # 连接相邻的点
    for curve in data["advancedCurveList"]:
        start_point = curve["startPos"]["instanceName"]
        end_point = curve["endPos"]["instanceName"]

        start_pos = next(point for point in points if point["instanceName"] == start_point)
        end_pos = next(point for point in points if point["instanceName"] == end_point)

        ax.plot([start_pos["pos"]["x"], end_pos["pos"]["x"]],
                [start_pos["pos"]["y"], end_pos["pos"]["y"]],
                [degree_dict[start_point], degree_dict[end_point]], color='b')
    # python

    ax.grid(True)
    # 设置图形的标签
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Degree')

    # 显示图形
    plt.show()
#     # print(json.dumps(a['advancedCurveList'][:10],indent=4))
#     points = data["advancedPointList"]
#     lines = data["advancedCurveList"]
#
#     # 统计每个点的度
#     degree = {}
#
#     # 1. 统计点的度
#     for line in lines:
#         start_point = line["startPos"]["pos"]
#         end_point = line["endPos"]["pos"]
#
#         # 统计每个点的出现次数
#         start_key = (start_point["x"], start_point["y"])
#         end_key = (end_point["x"], end_point["y"])
#
#         if start_key not in degree:
#             degree[start_key] = 0
#         if end_key not in degree:
#             degree[end_key] = 0
#
#         degree[start_key] += 1
#         degree[end_key] += 1
#
#     # 2. 获取点的坐标及其度
#     point_coords = {}
#     for point in points:
#         pos = point["pos"]
#         coords = (pos["x"], pos["y"])
#         point_coords[coords] = pos
#
#     # 3. 为点添加 Z 坐标（假设度数作为 Z 值）
#     point_z = {coords: degree.get(coords, 0) for coords in point_coords}
#
#     # 4. 绘制三维图
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#
#     # 将所有点绘制出来
#     x_vals = [pos["x"] for pos in point_coords.values()]
#     y_vals = [pos["y"] for pos in point_coords.values()]
#     z_vals = [point_z[(pos["x"], pos["y"])] for pos in point_coords.values()]
#
#     ax.scatter(x_vals, y_vals, z_vals, c=z_vals, cmap='viridis', s=50)
#
#     # 5. 绘制线路
#     # for line in lines:
#     #     start_pos = line["startPos"]["pos"]
#     #     end_pos = line["endPos"]["pos"]
#     #
#     #     x_line = [start_pos["x"], end_pos["x"]]
#     #     y_line = [start_pos["y"], end_pos["y"]]
#     #     z_line = [point_z[(start_pos["x"], start_pos["y"])], point_z[(end_pos["x"], end_pos["y"])]]
#     #
#     #     ax.plot(x_line, y_line, z_line, c='k', linewidth=1)
#     # 在绘制线路时使用平滑的曲线
#     for line in lines:
#         start_pos = line["startPos"]["pos"]
#         end_pos = line["endPos"]["pos"]
#         z_start = point_z[(start_pos["x"], start_pos["y"])]
#         z_end = point_z[(end_pos["x"], end_pos["y"])]
#
#         smoothed_points = smooth_curve(start_pos, end_pos, z_start, z_end)
#
#         # 绘制平滑的曲线
#         ax.plot(smoothed_points[:, 0], smoothed_points[:, 1], smoothed_points[:, 2], c='k', linewidth=1)
#
#     # 6. 设置标题和标签
#     ax.set_title("Point Degree in 3D Space")
#     ax.set_xlabel("X")
#     ax.set_ylabel("Y")
#     ax.set_zlabel("Degree (Z)")
#
#     plt.show()
#
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import json
#
# # 假设你已经从.smap文件读取并转换为data（JSON格式）
# data = {
#     "advancedPointList": [
#         {"className": "LocationMark", "instanceName": "LM1", "pos": {"x": -75.173, "y": -40.529},
#          "property": [{"key": "spin", "type": "bool", "value": "ZmFsc2U=", "boolValue": False}], "ignoreDir": True},
#         {"className": "LocationMark", "instanceName": "LM2", "pos": {"x": -74.173, "y": -40.529},
#          "property": [{"key": "spin", "type": "bool", "value": "ZmFsc2U=", "boolValue": False}], "ignoreDir": True},
#         {"className": "LocationMark", "instanceName": "LM3", "pos": {"x": -73.173, "y": -40.529},
#          "property": [{"key": "spin", "type": "bool", "value": "ZmFsc2U=", "boolValue": False}], "ignoreDir": True}
#     ],
#     "advancedCurveList": [
#         {"className": "DegenerateBezier", "instanceName": "LM1-PP4",
#          "startPos": {"instanceName": "LM1", "pos": {"x": -75.173, "y": -40.529}},
#          "endPos": {"instanceName": "LM2", "pos": {"x": -74.173, "y": -40.529}},
#          "controlPos1": {"x": -74.088, "y": -40.529}, "controlPos2": {"x": -73.004, "y": -40.529},
#          "property": [{"key": "direction", "type": "int", "value": "MA==", "int32Value": 0},
#                       {"key": "movestyle", "type": "int", "value": "MA==", "int32Value": 0}]},
#         {"className": "DegenerateBezier", "instanceName": "LM2-PP5",
#          "startPos": {"instanceName": "LM2", "pos": {"x": -74.173, "y": -40.529}},
#          "endPos": {"instanceName": "LM3", "pos": {"x": -73.173, "y": -40.529}},
#          "controlPos1": {"x": -73.088, "y": -40.529}, "controlPos2": {"x": -72.004, "y": -40.529},
#          "property": [{"key": "direction", "type": "int", "value": "MA==", "int32Value": 0},
#                       {"key": "movestyle", "type": "int", "value": "MA==", "int32Value": 0}]}
#     ]
# }


# import matplotlib.pyplot as plt
#
# from mpl_toolkits.mplot3d import axes3d
#
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
#
# # Grab some test data.
# X, Y, Z = axes3d.get_test_data(0.05)
#
# # Plot a basic wireframe.
# ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
#
# plt.show()


"""0106笔记"""
path = r"C:\Users\seer\Desktop\ruijie1230.smap"
tes = BeautifulSmap(path)
# print(json.dumps(tes.data,indent=4))
# print(tes.get_enclosure_pos([-28, -22, 0.6, 1.8]))
# a=tes.update_distribution_point([-28,-22.8,0.6,1.8])
print(tes.get_pos_by_name(names=["PP2", "AP3", "SM5", "CP4", "LM1"]))
# print(tes.update_lines(a))
# print(json.dumps(tes.data,indent=4))
# tes.add_point(type="LM",name="LM2",coordinates=(-75,-40))
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# 提取点位数据
points = tes.data['advancedPointList']
names = [point['instanceName'] for point in points]
x_vals = [point['pos']['x'] for point in points]  # 经度
y_vals = [point['pos']['y'] for point in points]  # 纬度

degree = defaultdict(int)
for curve in tes.data['advancedCurveList']:
    start_point = curve['startPos']['instanceName']
    end_point = curve['endPos']['instanceName']
    degree[start_point] += 1
    degree[end_point] += 1
# print(2,sum([1 for i in degree.values() if i==2]))
# print(4,sum([1 for i in degree.values() if i==4]))
# print(6,sum([1 for i in degree.values() if i==6]))
# # 设置颜色：度为1的点使用蓝色，度大于1的点使用红色
colors = tes.generate_random_colors(num_colors=16)

color_map = [colors[degree[name] - 1] for name in names]

# 提取线路数据（贝塞尔曲线的端点和控制点）
curves = tes.data['advancedCurveList']
curve_lines = []

for curve in curves:
    start_pos = curve['startPos']['pos']
    end_pos = curve['endPos']['pos']
    control1 = curve['controlPos1']
    control2 = curve['controlPos2']

    # 贝塞尔曲线公式绘制
    t = np.linspace(0, 1, 100)  # 曲线的参数，生成100个点
    x_curve = (1 - t) ** 3 * start_pos['x'] + 3 * (1 - t) ** 2 * t * control1['x'] + 3 * (1 - t) * t ** 2 * \
              control2['x'] + t ** 3 * end_pos['x']
    y_curve = (1 - t) ** 3 * start_pos['y'] + 3 * (1 - t) ** 2 * t * control1['y'] + 3 * (1 - t) * t ** 2 * \
              control2['y'] + t ** 3 * end_pos['y']

    curve_lines.append((x_curve, y_curve))

# 创建图形
plt.figure(figsize=(8, 6))

# 绘制所有点位，根据度设置颜色
plt.scatter(x_vals, y_vals, color=color_map, label='Location Marks')

# 为每个点位添加标签
for i, name in enumerate(names):
    plt.text(x_vals[i], y_vals[i], name, fontsize=12, ha='right', color=color_map[i])

# 绘制所有线路（贝塞尔曲线）
for i, (x_curve, y_curve) in enumerate(curve_lines):
    plt.plot(x_curve, y_curve, color='red')

# 设置图形标题和标签
plt.title('Geographical Points and Curves with Degree-based Colors')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# 显示图例
plt.legend()

# 显示图形
plt.grid(True)
plt.savefig("demo2.png")
plt.show()

