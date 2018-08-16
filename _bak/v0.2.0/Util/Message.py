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
        }

