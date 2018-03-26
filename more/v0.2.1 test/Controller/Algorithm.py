# -*- coding: utf-8 -*-

''' ***** 计算包 ***** '''
import numpy as np
import pywt #小波分析包


def MyCWT(data):
    pass
    #--原始数据初始化--
    #x = np.arange(len(data))
    y = data

    # Fs = 500000 #采样频率：500 000 Hz 
    #             #采样周期：2 us
    #--尺度计算--
    wavename = 'gaus1'
    totalscal = 64    #尺度序列的长度
    
    #Fc = 2000;          #小波中心频率(Hz)（“主波峰之间的差值”=2000Hz）
                        #Fc = pywt.central_frequency(wavename, precision=8) 
    Fc = pywt.central_frequency(wavename)               
                   
    C = 2*Fc*totalscal # C 为常数，C = 2*Fc/totalscal
    scal= C/np.arange(1,totalscal+1)   #尺度序列,范围（2*Fc,inf）

    #--连续小波变换--
    coef,freqs = pywt.cwt(y,scal,wavename)
    return coef,freqs
