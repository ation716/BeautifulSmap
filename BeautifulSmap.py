import os
import sys

p = os.path.abspath(__file__)
p = os.path.dirname(p)
sys.path.append(p)
import json
import colorsys
import random
import numpy as np
import config as cg
import math


# import pytest


class BeautifulSmap():
    """"""

    def __init__(self, spath):
        """"""
        self.spath = spath  # smap path
        self.file = open(file=self.spath, mode="r+b")
        self.__data = None  # smap data
        self.write_flag = False  # If modified, the source file will be overwritten.

    def __del__(self):
        """
        If modified, the source file will be overwritten.Then the file will be closed
        """
        if self.write_flag:
            self.file.truncate(0)
            json_m = json.dumps(self.data)
            json_m = json_m.encode('utf-8')
            self.file.write(json_m)
        print("close file")
        self.file.close()

    def __str__(self):
        return str(self.data)

    @property
    def data(self):
        """ smap data, json format """
        if self.__data is None:
            print("assign self.data")
            self.__data = json.load(self.file)
            self.file.seek(0)
        return self.__data

    @staticmethod
    def _if_in_rectangle(pos: tuple, rect: tuple):
        """
        :param pos: (x,y)
        :param rect: (-x,x,-y,y)
        :return bool
        """
        if isinstance(pos, tuple):
            return rect[0] <= pos[0] <= rect[1] and rect[2] <= pos[1] <= rect[3]
        if isinstance(pos, dict):
            return rect[0] <= pos['x'] <= rect[1] and rect[2] <= pos['y'] <= rect[3]

    @staticmethod
    def _generate_random_colors(num_colors: int):
        """
        :param num_colors:
        :return list
        """
        colors = []
        s, b = random.randint(0, 1), random.randint(0, 1)
        for i in range(num_colors):
            hue = 1 / num_colors  # 色调
            saturation = 0.7 + 0.3 * math.sin(i * math.pi / num_colors + s)  # 饱和度
            brightness = 0.5 + 0.5 * math.sin(i * math.pi / num_colors + b)  # 亮度
            rgb = colorsys.hsv_to_rgb(hue, saturation, brightness)
            colors.append(rgb)
        return colors
    @staticmethod
    def _get_tr(pos1,pos2):
        """"""
        p1,p2=pos1,pos2 if pos1[0]<pos2[0] else pos2,pos1
        return ((2*p1[0]+p2[0])/3, (2*p1[1]+p2[1])/3),((p1[0]+2*p2[0])/3, (p1[1]+2*p2[1])/3),

    @staticmethod
    def _ordered_sample(data_list: list, k: int):
        """在有序序列中随机选出长度为k的有序子集
        :param data_list: 有序序列
        :param k: 子集长度
        :return 有序子集
        """
        indices = random.sample(range(len(data_list)), k)
        sample = [data_list[i] for i in sorted(indices)]
        return sample

    def get_pos_by_name(self, names: list):
        """通过名字获取点位信息
        :param names: 点位名称表
        :return json：{name：{坐标：（），朝向：，随动：}}
        """
        if isinstance(names, str):
            names = [names]
        rlt = {}
        for pos in self.data.get("advancedPointList"):
            if pos['instanceName'] in names:
                rlt.setdefault(pos['instanceName'], {}).setdefault('coordinate', (pos['pos']['x'], pos['pos']['y']))
                if not pos.get('ignoreDir'):
                    if pos.get('dir') is None:
                        rlt[pos['instanceName']].setdefault('dir', 0)
                    else:
                        rlt[pos['instanceName']].setdefault('dir', pos['dir'])
                for p in pos['property']:
                    rlt[pos['instanceName']].setdefault(p['key'], p['boolValue'])
        return rlt

    def _get_pos_index_by_name(self, names: list):
        """通过点为名获取点位索引
        :param names: 点位名称表
        :return json: [i1,i2,...] , index= -1 代表未找到
        """
        if isinstance(names, str):
            names = [names]
        rlt = [-1 for _ in names]
        for i, pos in enumerate(self.data.get("advancedPointList")):
            if pos['instanceName'] in names:
                rlt[names.index(pos['instanceName'])] = i
        return rlt

    def _get_path_index_by_name(self,names: list):
        """"""
        if isinstance(names, str):
            names = [names]
        rlt = [-1 for _ in names]
        for i, pos in enumerate(self.data.get("advancedCurveList")):
            if pos['instanceName'] in names:
                rlt[names.index(pos['instanceName'])] = i
        return rlt

    def _get_pos_index_from_enclosure(self, rect: list = None, prefix: str = ""):
        """
        获取矩形区域的所有点位, 返回索引序列
        :param rect: (-x,x,-y,y)
        :param prefix: 点位前缀,做筛选用
        :return [i1,i2,i3,i4,...]
        """
        indexlist = []
        for i in range(len(self.data.get("advancedPointList"))):
            if self._if_in_rectangle(self.data.get("advancedPointList")[i]['pos'], rect):
                if prefix:
                    if self.data.get("advancedPointList")[i]['instanceName'].startswith(prefix):
                        indexlist.append((i,self.data.get("advancedPointList")[i]['pos']['x']))
                else:
                    indexlist.append((i,self.data.get("advancedPointList")[i]['pos']['x']))
        print(indexlist)
        sorted(indexlist,key=lambda x: x[1])
        return indexlist

    def get_pos_from_enclosure(self, rect: list = None, prefix=None):
        """获取矩形区域的所有点位, 点位为LM，AP，PP，CP，SM，不包含库位
        :param rect: (-x,x,-y,y)
        :param prefix: 点位前缀,做筛选用
        :return 点位列表
        """
        namelist = []
        for pos in self.data.get("advancedPointList"):
            if self._if_in_rectangle(pos['pos'], rect):
                if prefix:
                    if pos["instanceName"].startswith(prefix):
                        namelist.append(pos["instanceName"])
                else:
                    namelist.append(pos["instanceName"])
        return namelist

    def _get_path_index_from_enclosure(self, rect: list = None, prefix=None):
        """获取矩形区域的所有线路, 只要起点和终点都在矩形区域内则视为线路在矩形区域内, 返回索引序列
        :param rect: (-x,x,-y,y)
        :param prefix: 点位前缀,做筛选用
        :return 索引列表
        """
        indexlist = []
        for i, p in enumerate(self.data.get("advancedCurveList")):
            if self._if_in_rectangle(p["startPos"]['pos'], rect):
                if self._if_in_rectangle(p["endPos"]['pos'], rect):
                    if prefix:
                        if p["startPos"]["instanceName"].startswith(prefix):
                            if p["endPos"]["instanceName"].startswith(prefix):
                                indexlist.append(i)
                    else:
                        indexlist.append(i)
        return indexlist

    def get_path_from_enclosure(self, rect: list = None, prefix=None):
        """
        """
        namelist = []
        for cur in self.data.get("advancedCurveList"):
            if self._if_in_rectangle(cur["startPos"]['pos'], rect):
                if self._if_in_rectangle(cur["endPos"]['pos'], rect):
                    if prefix:
                        if cur["startPos"]["instanceName"].startswith(prefix):
                            if cur["endPos"]["instanceName"].startswith(prefix):
                                namelist.append(tuple(cur["instanceName"].split("-")))
                    else:
                        namelist.append(tuple(cur["instanceName"].split("-")))
        return namelist

    def add_normal_vertex_line(self, start: tuple, end: tuple, num):
        """增加点云"""
        l1 = np.linspace(start[0], end[0], num, dtype=float)
        l2 = np.linspace(start[1], end[1], num, dtype=float)
        if self.data.get("normalPosList") is None:
            self.data["normalPosList"] = []
        for z in zip(l1, l2):
            self.data["normalPosList"].append({'x': float(z[0]), 'y': float(z[1])})
        self.write_flag = True

    def del_normal_vertex(self):
        """删除所有点云"""
        self.data.pop("normalPosList")
        self.write_flag = True

    def add_pos(self, **kwargs):
        """ 增加点位, 不检查是否有重复点位
        :param kwargs:
            name: 点位名称, 符合调度名称规则 LM PP CP AP SM
            coordinates: 坐标（x,y）
            spin: 是否随动
            ignoreDir: 是否忽略朝向
            dir: 朝向, 弧度单位
        """
        if kwargs.get("name") and kwargs.get("coordinates"):
            if cg.pmodel.get(kwargs.get("type")):
                tem = cg.pmodel[kwargs.get("type")]
                tem["instanceName"] = kwargs.get("name")
                tem["pos"] = {"x": kwargs.get("coordinates")[0], "y": kwargs.get("coordinates")[1]}
                if kwargs.get('dir'):
                    tem.pop("ignoreDir", None)
                    tem["dir"] = kwargs.get("dir")
                if kwargs.get('spin'):
                    for prop in tem.get("property", []):
                        if prop["key"] == "spin":
                            prop["boolValue"] = kwargs.get("spin")
                self.write_flag = True
                self.data["advancedPointList"].append(tem)

    def add_path(self,rect: list = None):
        """将点位从左到右串联起来"""
        data={'className': 'DegenerateBezier', 'instanceName': 'SM5-LM1', 'startPos': {'instanceName': 'SM5', 'pos': {'x': -73.793, 'y': -39.401}}, 'endPos': {'instanceName': 'LM1', 'pos': {'x': -76.494, 'y': -39.292}}, 'controlPos1': {'x': -74.693, 'y': -39.365}, 'controlPos2': {'x': -75.594, 'y': -39.328}, 'property': [{'key': 'direction', 'type': 'int', 'value': 'MA==', 'int32Value': 0}, {'key': 'movestyle', 'type': 'int', 'value': 'MA==', 'int32Value': 0}]},
        a=self._get_pos_index_from_enclosure(rect=rect)
        for i in range(len(a)-1):
            c1,c2=self._get_tr(self.data['advancedPointList'][i])
            pass


        pass

    def delete_pos(self, names: list = None):
        """删除点位
        """
        self.write_flag = True
        if isinstance(names, str):
            names = [names]
        pos_len = len(self.data.get("advancedPointList"))
        for i, v in enumerate(self.data.get("advancedPointList")[::-1]):
            if v["instanceName"] in names:
                self.data.get("advancedPointList").pop(pos_len - i - 1)
        if self.data.get("advancedCurveList") is None:
            return
        path_len = len(self.data.get("advancedCurveList"))
        for i, cur in enumerate(self.data.get("advancedCurveList")[::-1]):
            if cur["startPos"]["instanceName"] in names:
                self.data.get("advancedCurveList").pop(path_len - i - 1)
                continue
            if cur["endPos"]["instanceName"] in names:
                self.data.get("advancedCurveList").pop(path_len - i - 1)
        if self.data.get("advancedCurveList") == []:
            self.data.pop("advancedCurveList")

    def update_trans(self, rect: tuple = None, names: list = None, prefix: str = "", x=0, y=0):
        """平移点位和线路
        1. 如果rect不为空,平移矩形区域内所有点位和线路
        2. names 不为空,所有点位 不考虑线路
        :param rect:
        :param names:
        :param x:
        :param y:
        :return None
        """
        indps,rlt = [],[]
        if rect is not None:
            indps = self._get_pos_index_from_enclosure(rect,prefix)
        else:
            indps = self._get_pos_index_by_name(names)
        for i in indps:
            if i==-1:
                continue
            self.data["advancedPointList"][i]["pos"]["x"] += x
            self.data["advancedPointList"][i]["pos"]["y"] += y
            rlt.append(self.data["advancedPointList"][i]["instanceName"])
        if rect is not None:
            indps2 = self._get_path_index_from_enclosure(rect,prefix)
            for i in indps2:
                path=self.data["advancedCurveList"][i]
                path["startPos"]["pos"]["x"]+=x
                path["startPos"]["pos"]["y"]+=y
                path["endPos"]["pos"]["y"]+=y
                path["endPos"]["pos"]["y"]+=y
                for c in path:
                    if c.startswith("controlPos"):
                        path[c]["x"]+=x
                        path[c]["y"]+=y
        self.write_flag = True
        return rlt

    def update_points(self,names):
        """"""

    def update_distribution_point(self, rect=None):
        """点位重新均匀分布
        :return {name:（x,y）}
        """
        namelist = []
        rlt = {}
        # print(len(self.data.get("advancedPointList")))
        for i in range(len(self.data.get("advancedPointList"))):
            if rect[0] < self.data.get("advancedPointList")[i]["pos"]["x"] < rect[1] and rect[2] < \
                    self.data.get("advancedPointList")[i]["pos"]["y"] < rect[3]:
                namelist.append(i)
        # print(namelist)
        namelist = sorted(namelist, key=lambda x: self.data["advancedPointList"][x]["pos"]["x"])
        minx = self.data["advancedPointList"][namelist[0]]["pos"]["x"]
        maxx = self.data["advancedPointList"][namelist[-1]]["pos"]["x"]
        # print(minx, maxx)
        uniform_x = np.linspace(minx, maxx, len(namelist))
        # print(namelist)
        # print(uniform_x)
        for i, x in zip(namelist, uniform_x):
            self.data["advancedPointList"][i]["pos"]["x"] = float(x)
            rlt.setdefault(self.data["advancedPointList"][i]["instanceName"], (
                self.data["advancedPointList"][i]["pos"]["x"], self.data["advancedPointList"][i]["pos"]["y"]))
        # print(rlt)
        return rlt

    def update_distribution_lines(self, pos: dict = None):
        """线路重新均匀分布
        """
        if pos is None:
            return
        self.write_flag = True
        rlt = []
        for i in self.data.get("advancedCurveList"):
            p = i["instanceName"].split("-")
            flag = False
            if pos.get(p[0]):
                i["startPos"]["pos"] = {"x": pos[p[0]][0], "y": pos[p[0]][1]}
                flag = True
            if pos.get(p[1]):
                i["endPos"]["pos"] = {"x": pos[p[1]][0], "y": pos[p[1]][1]}
                flag = True
            if flag:
                rlt.append(p)
                controlx = np.linspace(i["startPos"]["pos"]["x"], i["endPos"]["pos"]["x"], 4)
                controly = np.linspace(i["startPos"]["pos"]["y"], i["endPos"]["pos"]["y"], 4)
                i["controlPos1"] = {"x": controlx[1], "y": controly[1]}
                i["controlPos2"] = {"x": controlx[2], "y": controly[2]}
        return rlt

    def update_curve(self,rect:list=None,names: list = None,prefix:str="",property:dict=None):
        """"""
        indps, rlt = [], []
        if property:
            return
        if rect is not None:
            indps = self._get_path_index_from_enclosure(rect, prefix)
        else:
            indps = self._get_pos_index_by_name(names)
        for i in indps:
            for pi,pro in enumerate(self.data["advancedCurveList"][i]["property"]):
                if pro["key"] == property["key"]:
                    self.data["advancedCurveList"][i]["property"][pi]=property
                    break
            else:
                self.data["advancedCurveList"][i]["property"].append(property)



        #
        #     self.data["advancedPointList"][i]["pos"]["y"] += y
        #     rlt.append(self.data["advancedPointList"][i]["instanceName"])
        # if rect is not None:
        #     indps2 = self._get_path_index_from_enclosure(rect, prefix)
        #     for i in indps2:
        #         path = self.data["advancedCurveList"][i]
        #         path["startPos"]["pos"]["x"] += x
        #         path["startPos"]["pos"]["y"] += y
        #         path["endPos"]["pos"]["y"] += y
        #         path["endPos"]["pos"]["y"] += y
        #         for c in path:
        #             if c.startswith("controlPos"):
        #                 path[c]["x"] += x
        #                 path[c]["y"] += y
        # self.write_flag = True
        # return rlt
        #
        # pass

    def strech(self, rect: list = None):
        """线路和点位重新拉伸,使得点位和线路均匀分布
        :param rect:(-x,x,-y,y)
        """
        pos = self.update_distribution_point(rect)
        self.update_distribution_lines(pos)

    # def update_curve(self, names: list = None):

    # def demo2(self, a):
    #     """
    #     """


if __name__ == '__main__':
    path = r"D:\workshop\new_bug\test_map.smap"
    tes = BeautifulSmap(path)
    tes.add_path(rect=(-80,-72,-39,-36))
    print(tes.data)
    # print(tes._get_pos_index_from_enclosure(rect=(-48, -15, 7, 9)))
    # print(tes.get_pos_from_enclosure(rect=(-48, -15, 7, 9)))
    # tes.add_path(rect=(-48,-15,7,9))
    # tes.update_curve()
    # tes.update_trans(rect=(-68,-62,-40,-38),x=-10)
    # tes.update_trans(rect=(-68,-62,-40,-38),x=-10)

    # print(tes.add_normal_pos((-79, -40), (-79, -35), 80))
    # print(json.dumps(tes.data['advancedCurveList'],indent=4))
    # tes.delete_pos(names=['AP3'])
    # a = [1, 2, 3, 4, 5, 6, 7]
    # print(tes._ordered_sample(a, 10))
    # print(json.dumps(tes.data['advancedCurveList'],indent=4))
    # datat1=jso
    # n.dumps(tes.data)
    # tes.delete_pos(names=["AP3"])
    # with open('test_map.', 'w') as f:
    #     f.write(json.dumps(tes.data))
    # print(tes)

    # data2=json.dumps(tes.data)
    # assert data1==data2
    # with open("tes_map2.py", "w") as f:
    #     f.write(json.dumps(tes.data,indent=4))
    # tes.add_pos(name="AP22",coordinates=(-80,-39),spin=True,dir=1,type="AP")
    # print(tes._get_path_index_from_enclosure((-81,-77,-40,-36)))
    # print(tes.get_path_from_enclosure((-81,-77,-40,-36)))
    # tes._if_in_rectangle()
    # # print(json.dumps(tes.data,indent=4))
    # print(tes.get_pos_from_enclosure([-6.5, -4, 0.5, 2.4]))
    # print(tes.get_pos_from_enclosure([-6.5, -4, -1.4, 0.5]))
    # print(tes.get_pos_from_enclosure([-6.5, -4, -4, -2]))
    # ids=tes.get_pos_index_from_enclosure([-7, -4, 0.3, 2])
    # new=tes.update_trans(ids, -2, 0)
    # print(tes.update_lines(new))

    # print(tes.get_enclosure_path([-80, -72, -40, -36]))
    # a=tes.update_distribution_point([-80, -72, -40, -36])
    # print(tes.get_pos_by_name(names=["PP2", "AP3","SM5","CP4","LM1"]))
    # # print(tes.update_lines(a))
    # # print(json.dumps(tes.data,indent=4))
    # # tes.add_point(type="LM",name="LM2",coordinates=(-75,-40))
    # import matplotlib.pyplot as plt
    # import numpy as np
    # from collections import defaultdict
    #
    # # 提取点位数据
    # points = tes.data['advancedPointList']
    # names = [point['instanceName'] for point in points]
    # x_vals = [point['pos']['x'] for point in points]  # 经度
    # y_vals = [point['pos']['y'] for point in points]  # 纬度
    #
    # degree = defaultdict(int)
    # for curve in tes.data['advancedCurveList']:
    #     start_point = curve['startPos']['instanceName']
    #     end_point = curve['endPos']['instanceName']
    #     degree[start_point] += 1
    #     degree[end_point] += 1
    # # print(2,sum([1 for i in degree.values() if i==2]))
    # # print(4,sum([1 for i in degree.values() if i==4]))
    # # print(6,sum([1 for i in degree.values() if i==6]))
    # # # 设置颜色：度为1的点使用蓝色，度大于1的点使用红色
    # colors=tes.generate_random_colors(num_colors=16)
    #
    # color_map = [colors[degree[name]-1] for name in names]
    #
    # # 提取线路数据（贝塞尔曲线的端点和控制点）
    # curves = tes.data['advancedCurveList']
    # curve_lines = []
    #
    # for curve in curves:
    #     start_pos = curve['startPos']['pos']
    #     end_pos = curve['endPos']['pos']
    #     control1 = curve['controlPos1']
    #     control2 = curve['controlPos2']
    #
    #     # 贝塞尔曲线公式绘制
    #     t = np.linspace(0, 1, 100)  # 曲线的参数，生成100个点
    #     x_curve = (1 - t) ** 3 * start_pos['x'] + 3 * (1 - t) ** 2 * t * control1['x'] + 3 * (1 - t) * t ** 2 * \
    #               control2['x'] + t ** 3 * end_pos['x']
    #     y_curve = (1 - t) ** 3 * start_pos['y'] + 3 * (1 - t) ** 2 * t * control1['y'] + 3 * (1 - t) * t ** 2 * \
    #               control2['y'] + t ** 3 * end_pos['y']
    #
    #     curve_lines.append((x_curve, y_curve))
    #
    # # 创建图形
    # plt.figure(figsize=(8, 6))
    #
    # # 绘制所有点位，根据度设置颜色
    # plt.scatter(x_vals, y_vals, color=color_map, label='Location Marks')
    #
    # # 为每个点位添加标签
    # for i, name in enumerate(names):
    #     plt.text(x_vals[i], y_vals[i], name, fontsize=12, ha='right', color=color_map[i])
    #
    # # 绘制所有线路（贝塞尔曲线）
    # for i, (x_curve, y_curve) in enumerate(curve_lines):
    #     plt.plot(x_curve, y_curve, color='red')
    #
    # # 设置图形标题和标签
    # plt.title('Geographical Points and Curves with Degree-based Colors')
    # plt.xlabel('Longitude')
    # plt.ylabel('Latitude')
    #
    # # 显示图例
    # plt.legend()
    #
    # # 显示图形
    # plt.grid(True)
    # plt.savefig("demo2.png")
    # plt.show()
    # from collections import defaultdict
    #
    #
    # # 构建图
    # def build_graph(edges):
    #     graph = defaultdict(list)
    #     for u, v in edges:
    #         graph[u].append(v)
    #     return graph
    #
    #
    # # 检测图中的环
    # def find_cycles(graph):
    #     def dfs(node, visited, rec_stack, cycle_path):
    #         visited[node] = True
    #         rec_stack[node] = True
    #         cycle_path.append(node)
    #
    #         # 访问邻接节点
    #         for neighbor in graph[node]:
    #             if not visited[neighbor]:
    #                 if dfs(neighbor, visited, rec_stack, cycle_path):
    #                     return True
    #             elif rec_stack[neighbor]:
    #                 # 找到环
    #                 cycle_path.append(neighbor)
    #                 return True
    #
    #         # 回溯时将当前节点从递归栈中移除
    #         rec_stack[node] = False
    #         cycle_path.pop()
    #         return False
    #
    #     # 遍历所有节点
    #     visited = {node: False for node in graph}
    #     rec_stack = {node: False for node in graph}
    #     cycles = []
    #
    #     for node in graph:
    #         if not visited[node]:
    #             cycle_path = []
    #             if dfs(node, visited, rec_stack, cycle_path):
    #                 cycles.append(cycle_path)
    #
    #     return cycles
    #
    #
    # nodes = ['LM1', 'PP2', 'AP3', 'CP4', 'SM5']
    # edges = [('PP2', 'AP3'), ('AP3', 'PP2'), ('AP3', 'SM5'), ('SM5', 'AP3'),
    #          ('SM5', 'LM1'), ('LM1', 'SM5'), ('LM1', 'CP4'), ('CP4', 'LM1'),
    #          ('PP2', 'CP4'), ('CP4', 'PP2')]
    #
    # # 构建图
    # graph = build_graph(edges)
    #
    # # 查找环
    # cycles = find_cycles(graph)
    #
    # # 输出环
    # print("环：")
    # print(cycles)
    # # for cycle in cycles:
    # #     print(" -> ".join(cycle))
