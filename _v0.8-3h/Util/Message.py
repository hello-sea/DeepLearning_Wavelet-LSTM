# -*- coding: utf-8 -*-

class Message():
    def __init__(self):
        self.dict = {
            # 正常
            0 : '0',
            # 软件运行错误
            'Error(0001)': 'Error(0001): 软件运行错误，请连续管理员！',
            # 文件数据错误
            'Error(1000)': 'Error(1000): Seg文件读取错误，请检测Seg数据！',
            'Error(1001)': 'Error(1001): Seg文件数据为空，请检测Seg数据！',
            'Error(1002)': 'Error(1002): 请正确选择文件！',
            # 用户操作失误
            'Warning(1001)': 'Warning(1001): 未加载数据,请先选择seg文件！',
            'Warning(1002)': 'Warning(1002): 未完成滤波,请先进行第2步滤波操作！',
            'Warning(1003)': 'Warning(1002): 未完成CWT分析,请先进行第3步CWT分析！'
        }

