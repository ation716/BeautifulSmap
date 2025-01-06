import sys
import os
p = os.path.abspath(__file__)
p = os.path.dirname(p)
sys.path.append(p)
import csv
import json
import colorsys
import os
import re
import networkx as nx      # networkx为第三方库,包含多种图论算法
import copy
import uuid
import math
import random
import numpy as np
import config as cg
# import config as cg
from enum import Enum


class BeautifulSmap():
    """"""

    def __init__(self,path):
        """"""
        self.path = path
        self.file=open(file=self.path, mode="r+b")
        self.__data=None
        self.write_flag=False

    def __del__(self):
        """"""
        print("close file")
        if self.write_flag:
            json_m=json.dumps(self.data)
            json_m=json_m.encode('utf-8')
            self.file.write(json_m)
        self.file.close()

    @property
    def data(self):
        """"""
        if self.__data is None:
            print("assign self.data")
            self.__data=json.load(self.file)
            self.file.seek(0)
        return self.__data
    @staticmethod
    def _if_in_rectangle(pos,rect):
        """
        :param pos: (x,y)
        :param rect: (-x,x,-y,y)
        :return bool
        """
        if isinstance(pos,tuple):
            return rect[0]<= pos[0] <= rect[1] and rect[2] <= pos[1] <= rect[3]
        if isinstance(pos,dict):
            return rect[0] <= pos['x'] <= rect[1] and rect[2] <= pos['y'] <= rect[3]



    def generate_random_colors(self,num_colors):
        colors = []
        for _ in range(num_colors):
            hue = random.random()  # 随机色调
            saturation = random.uniform(0.7, 1)  # 随机饱和度
            brightness = random.uniform(0.3, 1)  # 随机亮度
            rgb = colorsys.hsv_to_rgb(hue, saturation, brightness)
            colors.append(rgb)
        return colors
    def get_pos_by_name(self,names):
        """通过名字获取点位信息
        :param names: list， str
        :return json：{name：{坐标：（），朝向：，随动：}}
        """
        res={}
        for pos in self.data.get("advancedPointList"):
            if pos['instanceName'] in names:
                res.setdefault(pos['instanceName'],{}).setdefault('coordinate',(pos['pos']['x'],pos['pos']['y']))
                if not pos.get('ignoreDir'):
                    if pos.get('dir') is None:
                        res[pos['instanceName']].setdefault('dir',0)
                    else:
                        res[pos['instanceName']].setdefault('dir', pos['dir'])
                for p in pos['property']:
                    res[pos['instanceName']].setdefault(p['key'], p['boolValue'])
        return res

    def get_coordinate_by_name(self,names):
        """
        :param names: list， str
        :return json：{name：{坐标：（），朝向：，随动：}}
        """

    def get_enclosure_pos_index(self, rect: list = None,prefix=None):
        """获取矩形区域的所有点位, 返回索引序列
        :param rect: (-x,x,-y,y)
        :param prefix: 点位前缀,做筛选用
        :return 点位索引列表
        """
        indexlist = []
        for i in range(len(self.data.get("advancedPointList"))):
            if self._if_in_rectangle(self.data.get("advancedPointList")[i]['pos'],rect):
                    if prefix:
                        if self.data.get("advancedPointList")[i]['instanceName'].startswith(prefix):
                            indexlist.append(i)
                    else:
                        indexlist.append(i)
        return indexlist

    def get_enclosure_pos(self,rect:list=None,prefix=None):
        """获取矩形区域的所有点位, 点位为LM，AP，PP，CP，SM，不包含库位
        :param rect: (-x,x,-y,y)
            :param prefix: 点位前缀,做筛选用
        :return 点位列表
        """
        namelist=[]
        for pos in self.data.get("advancedPointList"):
            if self._if_in_rectangle(pos['pos'],rect):
                if prefix:
                    if pos["instanceName"].startswith(prefix):
                        namelist.append(pos["instanceName"])
                else:
                    namelist.append(pos["instanceName"])
        return namelist

    def get_enclosure_path_index(self,rect:list=None,prefix=None):
        """获取矩形区域的所有线路, 只要起点和终点都在矩形区域内则视为线路在矩形区域内, 返回索引序列
        """
        indexlist = []
        for i in range(len(self.data.get("advancedCurveList"))):
            if self._if_in_rectangle(self.data.get("advancedCurveList")[i]["startPos"]['pos'],rect):
                if self._if_in_rectangle(self.data.get("advancedCurveList")[i]["endPos"]['pos'], rect):
                    if prefix:
                        if self.data.get("advancedCurveList")[i]["startPos"]["instanceName"].startswith(prefix):
                            if self.data.get("advancedCurveList")[i]["endPos"]["instanceName"].startswith(prefix):
                                indexlist.append(i)
                    else:
                        indexlist.append(i)
        return indexlist

    def get_enclosure_path(self,rect:list=None,prefix=None):
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

    def add_point(self,**kwargs):
        """ 增加点位, 不检查是否有重复点位
        :param kwargs:
            type 点位类型
            name: 点位名称
            coordinates: 坐标（x,y）
            # spin: 是否随动
            # ignoredir: 是否有朝向
        """
        if cg.pmodel.get(kwargs.get("type")):
            tem=cg.pmodel[kwargs.get("type")]
            tem["instanceName"]=kwargs.get("name")
            tem["pos"]={"x":kwargs.get("coordinates")[0],"y":kwargs.get("coordinates")[1]}
            self.write_flag=True
            self.data["advancedPointList"].append(tem)

    def delete(self):
        """"""
        pass

    def update_trans(self):
        """平移点位"""
        pass

    def update_points(self):
        """"""

    def update_distribution_point(self,rect=None):
        """点位重新均匀分布
        :return {name:（x,y）}
        """
        namelist=[]
        result={}
        # print(len(self.data.get("advancedPointList")))
        for i in range(len(self.data.get("advancedPointList"))):
            if rect[0] < self.data.get("advancedPointList")[i]["pos"]["x"] < rect[1] and rect[2] <self.data.get("advancedPointList")[i]["pos"]["y"] < rect[3]:
                namelist.append(i)
        print(namelist)
        namelist=sorted(namelist,key=lambda x:self.data["advancedPointList"][x]["pos"]["x"])
        minx=self.data["advancedPointList"][namelist[0]]["pos"]["x"]
        maxx=self.data["advancedPointList"][namelist[-1]]["pos"]["x"]
        print(minx,maxx)
        uniform_x=np.linspace(minx,maxx,len(namelist))
        print(namelist)
        print(uniform_x)
        for i,x in zip(namelist,uniform_x):
            self.data["advancedPointList"][i]["pos"]["x"]=float(x)
            result.setdefault(self.data["advancedPointList"][i]["instanceName"],(self.data["advancedPointList"][i]["pos"]["x"],self.data["advancedPointList"][i]["pos"]["y"]))
        print(result)
        return result

    def update_lines(self,pos:dict=None):
        """线路重新均匀分布

        """
        if pos is None:
            return
        self.write_flag=True
        result=[]
        for i in self.data.get("advancedCurveList"):
            p=i["instanceName"].split("-")
            flag=False
            if pos.get(p[0]):
                i["startPos"]["pos"]={"x":pos[p[0]][0],"y":pos[p[0]][1]}
                flag=True
            if pos.get(p[1]):
                i["endPos"]["pos"] = {"x": pos[p[1]][0], "y": pos[p[1]][1]}
                flag=True
            if flag:
                result.append(p)
                controlx=np.linspace(i["startPos"]["pos"]["x"],i["endPos"]["pos"]["x"] , 4)
                controly=np.linspace(i["startPos"]["pos"]["y"],i["endPos"]["pos"]["y"] , 4)
                i["controlPos1"]={"x":controlx[1],"y":controly[1]}
                i["controlPos2"]={"x":controlx[2],"y":controly[2]}
        return result

    def strech(self,rect:list=None):
        """线路和点位重新拉伸
        :param rect:(-x,x,-y,y)
        """
        pos=self.update_distribution_point(rect)
        self.update_lines(pos)




    def demo2(self,a):
        """

        """


if __name__ == '__main__':
    path=r"C:\Users\seer\Desktop\test_map.smap"
    tes=BeautifulSmap(path)
    # print(json.dumps(tes.data,indent=4))
    print(tes.get_enclosure_pos([-80, -72, -40, -36]))
    print(tes.get_enclosure_path([-80, -72, -40, -36]))
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
    from collections import defaultdict


    # 构建图
    def build_graph(edges):
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
        return graph


    # 检测图中的环
    def find_cycles(graph):
        def dfs(node, visited, rec_stack, cycle_path):
            visited[node] = True
            rec_stack[node] = True
            cycle_path.append(node)

            # 访问邻接节点
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    if dfs(neighbor, visited, rec_stack, cycle_path):
                        return True
                elif rec_stack[neighbor]:
                    # 找到环
                    cycle_path.append(neighbor)
                    return True

            # 回溯时将当前节点从递归栈中移除
            rec_stack[node] = False
            cycle_path.pop()
            return False

        # 遍历所有节点
        visited = {node: False for node in graph}
        rec_stack = {node: False for node in graph}
        cycles = []

        for node in graph:
            if not visited[node]:
                cycle_path = []
                if dfs(node, visited, rec_stack, cycle_path):
                    cycles.append(cycle_path)

        return cycles


    nodes = ['LM1', 'PP2', 'AP3', 'CP4', 'SM5']
    edges = [('PP2', 'AP3'), ('AP3', 'PP2'), ('AP3', 'SM5'), ('SM5', 'AP3'),
             ('SM5', 'LM1'), ('LM1', 'SM5'), ('LM1', 'CP4'), ('CP4', 'LM1'),
             ('PP2', 'CP4'), ('CP4', 'PP2')]

    # 构建图
    graph = build_graph(edges)

    # 查找环
    cycles = find_cycles(graph)

    # 输出环
    print("环：")
    print(cycles)
    # for cycle in cycles:
    #     print(" -> ".join(cycle))