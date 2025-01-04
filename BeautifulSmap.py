import sys
import os
p = os.path.abspath(__file__)
p = os.path.dirname(p)
sys.path.append(p)
import csv
import json
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

    def get_pos_by_name(self,name):
        """通过名字获取点位信息"""
    def get_enclosure_pos_index(self, rect: list = None):
        """获取矩形区域的所有点位, 返回索引序列
        :param rect: (-x,x,-y,y)
        :return 点位列表
        """
        namelist = []
        for i in range(len(self.data.get("advancedPointList"))):
            if rect[0] < self.data.get("advancedPointList")[i]["pos"]["x"] < rect[1]:
                if rect[2] < self.data.get("advancedPointList")[i]["pos"]["y"] < rect[3]:
                    namelist.append(i)
        return namelist
    def get_enclosure_pos(self,rect:list=None):
        """获取矩形区域的所有点位, 点位为LM，AP，PP，CP，SM，不包含库位
        :param rect: (-x,x,-y,y)
        :return 点位列表
        """
        namelist=[]
        for pos in self.data.get("advancedPointList"):
            if rect[0]<pos["pos"]["x"]<rect[1] and rect[2]<pos["pos"]["y"]<rect[3]:
                namelist.append(pos["instanceName"])
        return namelist

    def add_point(self,**kwargs):
        """ 增加点位, 不检查是否有重复点位
        :param kwargs:
            type 点位类型
            name: 点位名称
            coordinates: 坐标（x,y）
            spin: 是否随动
            ignoredir: 是否有朝向
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
    # print(tes.get_enclosure_pos([-28, -22, 0.6, 1.8]))
    # a=tes.update_distribution_point([-28,-22.8,0.6,1.8])

    # print(tes.update_lines(a))
    print(json.dumps(tes.data,indent=4))
    # tes.add_point(type="LM",name="LM2",coordinates=(-75,-40))
    pass