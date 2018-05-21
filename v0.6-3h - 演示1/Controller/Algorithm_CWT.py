# -*- coding: utf-8 -*-

''' ***** 计算包 ***** '''
import numpy as np
import pywt #小波分析包

from scipy import signal
from sklearn import preprocessing 

from sklearn.preprocessing.data import minmax_scale # 0-1 标准化
 
from wavelets import Morlet,cwt, WaveletAnalysis
# https://github.com/aaren/wavelets
# pip install git+https://github.com/aaren/wavelets

def MyPywtCWT(data):
    pass
    ''' --原始数据信息初始化--'''

    # Fs = 500000 #采样频率：500 000 Hz ; 采样周期：2 us
    ''' --尺度计算-- '''
    wavename = 'gaus1'
    totalscal = 256          #尺度序列的长度
    
    #Fc = 2000;             #小波中心频率(Hz)（“主波峰之间的差值”=2000Hz）
    #Fc = pywt.central_frequency(wavename, precision=8) 
    Fc = pywt.central_frequency(wavename)               
                   
    C = 2*Fc*totalscal      # C为常数,用于计算尺度序列. C = 2*Fc/totalscal
    scal= C/np.arange(1,totalscal+1)    #尺度序列,范围（2*Fc,inf）

    #--连续小波变换--
    coef,freqs = pywt.cwt(data, scal, wavename)
    coef = np.abs(coef)
    return coef,freqs


def MyScipyCwt(data,MyWidths):
    ''' 将int型data转为float型sig '''
    sig = np.ones(len(data),np.float)  #产生空的float型sig
    for i in range(0,len(data)): 
        sig[i] = float(data[i])

    # widths = np.arange(1, 31)
    widths = np.arange(1, MyWidths+1)
    ''' 
    signal.cwt(sig, signal.ricker, widths) 
        - CWT: Continuous wavelet transform 连续小波变换
        - signal.ricker返回一个Ricker小波，也被称为“墨西哥帽子小波”   
    '''
    cwtmatr =  signal.cwt(sig, signal.ricker, widths) 
    # cwtmatr = np.abs(cwtmatr)
    # plt.imshow(cwtmatr, extent=[-1, 1, 31, 1], cmap='PRGn', aspect='auto', vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
    return cwtmatr


def MyWavelets(data,MyWidths):
    Widths = MyWidths

    ''' 将int型data转为float型sig '''
    sig = np.ones(len(data),np.float)  #产生空的float型sig
    for i in range(0,len(data)): 
        sig[i] = float(data[i])

    sig = np.array( sig )
    wa = WaveletAnalysis(sig, wavelet=Morlet() )
    # wavelet power spectrum
    power = wa.wavelet_power

    # scales 
    scales = wa.scales

    # associated time vector
    t = wa.time

    # reconstruction of the original data
    rx = wa.reconstruction()
    

    ########################################
    # print(power.shape)
    # power = np.transpose(power) #转置
    power = power.T
    # print(power.shape)

    # # 数据逐帧 0-1标准化
    # power_out = []
    # for i in power:
    # #     # np.append(power_out, minmax_scale(i), axis = 0)
    #     # power_out.append( minmax_scale(i).tolist() )
    #     power_out.append( minmax_scale(i))
    #     # print(max( minmax_scale(i) ))
    # # power_out = np.array(power_out)


    # return power_out
    return power


if __name__ == "__main__":   
    '''
    # import pywt
    # import numpy as np
    # import matplotlib.pyplot as plt
    # x = np.arange(512)
    # y = np.sin(2*np.pi*x/32)
    # coef, freqs=pywt.cwt(y,np.arange(1,129),'gaus1')
    # plt.matshow(coef) 
    # plt.show() 
    '''

    '''
    import pywt
    import numpy as np
    import matplotlib.pyplot as plt
    t = np.linspace(-1, 1, 200, endpoint=False)
    sig  = np.cos(2 * np.pi * 7 * t) + np.real(np.exp(-7*(t-0.4)**2)*np.exp(1j*2*np.pi*2*(t-0.4)))
    widths = np.arange(1, 31)
    cwtmatr, freqs = pywt.cwt(sig, widths, 'mexh')
    plt.imshow(cwtmatr, extent=[-1, 1, 1, 31], cmap='PRGn', aspect='auto',
           vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())  
    plt.show() 
    '''


    


    








