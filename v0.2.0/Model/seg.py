# -*- coding: utf-8 -*-

import struct
from PyQt5 import QtWidgets


class DataTtrack():
    def __init__(self):
        self.headBegin = None   # 道数据（测点头）开始指针下标
        self.dataBegin = None   # 采样数据开始指针下标   240
        self.dataNum = None  # 采集数目 114~115  (5120点)
        self.sampleInterval = None  # 记录每一次采样间隔 116-117 （除以5）
        self.waveSpeed = None   # 波速 238-239


class Seg():
    def __init__(self):
        pass

    def setupMainWindows(self, MainWindows):
        self.MainWindows = MainWindows

    def loadFile(self, fileName):
        self.fileName = fileName
        self.file = open(self.fileName, "rb")
        try:
            self.fileData = self.file.read()

            if(len(self.fileData) == 0):
                return 'Error(1001)'
            else:
                return self.initData()
        except:
            return 'Error(1000)'
        finally:
            self.file.close()

    def initData(self):
        '''
            seg文件格式的读取，严格执行seg文件格式标准
            seg文件分为两部分：
                >(一个) 文件头(部) * 3600字节
                >(多个) 道头(240字节) 和 地震数据
        '''
        ''' 1.(一个) 文件头(部) *3600字节 （3200字节文件头+400字节二进制文件头）'''

        # 测点数据总道数   0000-0001
        self.tapeNum = self.fileData[0] + self.fileData[1]*256
        # 测点数据数组下标（指针）4个字节 0002-2997
        self.arrayIndex = self.fileData[2:2997]
        # 记录文件是否有效,0为有效 2999-3000
        self.fileJudge = self.fileData[2999] + self.fileData[3000]*256
        # 400字节二进制文件头
        self.reel = self.fileData[3200:3599]

        ''' 2.(多个) 道头(240字节) + 数据体 '''
        self.dataList = []
        for i in range(0, self.tapeNum):  # range(A,B)函数: A,A+1,***,(B-1)
            data = DataTtrack()
            # 2.1 道头(240*Byte)
            if i == 0:
                data.headBegin = 3600
            else:
                data.headBegin = self.dataList[i - 1].dataBegin + self.dataList[i-1].dataNum*2
            data.dataBegin = data.headBegin + 240
            data.dataNum = self.fileData[data.headBegin + 114] + self.fileData[data.headBegin+115] * 256
            data.sampleInterval = (self.fileData[data.headBegin+116] + self.fileData[data.headBegin+117] * 256)/5
            data.waveSpeed = self.fileData[data.headBegin + 238] + self.fileData[data.headBegin+239] * 256
            # 2.2 数据体
            pass
            self.dataList.append(data)

        return 0
