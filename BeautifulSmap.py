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
# import config as cg
from enum import Enum


class BeautifulSmap:
    """"""

    def __init__(self,path):
        """"""
        self.path = path
        self.file=open(file=self.path, mode="rb+")
        self.__data=None
        self.write_flag=False

    def __del__(self):
        """"""
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
    def demo(self):
        """"""
        a=self.data
        pass

    def get_rect(self,rect=None):
        """获取矩形区域的所有点位
        :param rect: -x,x,-y,y
        """
        namelist=[]
        for pos in self.data.get("advancedPointList"):
            if rect[0]<pos["pos"]["x"]<rect[1] and rect[2]<pos["pos"]["y"]<rect[3]:
                namelist.append(pos["instanceName"])
        print(namelist)
        return namelist
    def add(self,data):
        """
        """

    def delete(self):
        """"""
        pass

    def update_trans(self):
        """平移点位"""
        pass

    def update_distribution_point(self,rect=None):
        """点位重新均匀分布"""
        namelist=[]
        # print(len(self.data.get("advancedPointList")))
        for i in range(len(self.data.get("advancedPointList"))):
            if rect[0] < self.data.get("advancedPointList")[i]["pos"]["x"] < rect[1] and rect[2] <self.data.get("advancedPointList")[i]["pos"]["y"] < rect[3]:
                namelist.append(i)
        print(namelist)
        namelist=sorted(namelist,key=lambda x:self.data["advancedPointList"][x]["pos"]["x"])
        minx=self.data["advancedPointList"][namelist[0]]["pos"]["x"]
        maxx=self.data["advancedPointList"][namelist[-1]]["pos"]["x"]
        uniform_x=np.linspace(minx,maxx,len(namelist))
        print(namelist)
        print(uniform_x)
        for i,x in zip(namelist,uniform_x):
            self.data["advancedPointList"][i]["pos"]["x"]=float(x)

    def update_distribution_line(self,rect=None):
        """线路重新均匀分布"""
        namelist = []
        # print(len(self.data.get("advancedPointList")))
        for i in range(len(self.data.get("advancedPointList"))):
            if rect[0] < self.data.get("advancedPointList")[i]["pos"]["x"] < rect[1] and rect[2] < \
                    self.data.get("advancedPointList")[i]["pos"]["y"] < rect[3]:
                namelist.append(i)
        print(namelist)
        namelist = sorted(namelist, key=lambda x: self.data["advancedPointList"][x]["pos"]["x"])
        minx = self.data["advancedPointList"][namelist[0]]["pos"]["x"]
        maxx = self.data["advancedPointList"][namelist[-1]]["pos"]["x"]
        uniform_x = np.linspace(minx, maxx, len(namelist))
        print(namelist)
        print(uniform_x)
        for i, x in zip(namelist, uniform_x):
            self.data["advancedPointList"][i]["pos"]["x"] = float(x)




if __name__ == '__main__':
    path=r"C:\Users\seer\Desktop\ruijie1230.smap"
    tes=BeautifulSmap(path)
    # tes.get_rect([-28,-22,0.6,1.8])
    # tes.update_distribution([-28,-22,0.6,1.8])
    tes.update_distribution([-28,-22,0.6,1.8])

    pass