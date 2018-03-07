# encoding: utf-8 
import numpy as np
from lstm import LstmParam, LstmNetwork

import pywt
import matplotlib.pyplot as plt

def MaxMinNormalization( x ):  # (0,1)标准化
    Max = 0
    Min = 0
    for i in x:
        if(Max < i ):
            Max = i
        if(Min > i ):
            Min = i
    for i in np.arange( len(x)):
        x[i] = (x[i] - Min) / (Max - Min)
    return x


class ToyLossLayer:
    """
    Computes square loss with first element of hidden layer array.
    计算 隐藏层数组的第一个元素的平方损失。
    """
    @classmethod
    def loss(self, pred, label):
        return (pred[0] - label) ** 2

    @classmethod
    def bottom_diff(self, pred, label):
        diff = np.zeros_like(pred)
        diff[0] = 2 * (pred[0] - label)
        return diff


def example_0(): #lstm
    # learns to repeat simple sequence from random inputs
    # 从随机输入重复简单的序列学习
    np.random.seed(0)

    # parameters for input data dimension and lstm cell count
    # 输入数据维度和lstm单元数量的参数
    mem_cell_ct = 100   # mem_cell_ct是lstm的神经元数目
    x_dim = 50          # x_dim是输入数据的维度
    lstm_param = LstmParam(mem_cell_ct, x_dim)
    lstm_net = LstmNetwork(lstm_param)  
    #y_list = [-0.5, 0.2, 0.1, -0.5]     #此 代码 其是通过自己实现 lstm 网络来逼近一个序列，y_list = [-0.5, 0.2, 0.1, -0.5]                        # 
    y_list = [-0.5, 0, -0.5] 
    input_val_arr = [np.random.random(x_dim) for _ in y_list]   # 输入

    #print(input_val_arr)
    for cur_iter in range(100000):
        print("iter", "%2s" % str(cur_iter), end=": ")
        for ind in range(len(y_list)):
            lstm_net.x_list_add(input_val_arr[ind])

        print("y_pred = [" +
              ", ".join(["% 2.5f" % lstm_net.lstm_node_list[ind].state.h[0] for ind in range(len(y_list))]) +
              "]", end=", ")

        loss = lstm_net.y_list_is(y_list, ToyLossLayer)
        print("loss:", "%.3e" % loss)
        lstm_param.apply_diff(lr=0.1)
        lstm_net.x_list_clear()


def example_1(): #vavelet
    filename = 'data.txt'  #txt文件和当前脚本在同一目录下，所以不用写具体路径
    data = []
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
                pass
            # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            p_tmp = lines.split() 
            data.append(p_tmp[0])  # 添加新读取的数据
            pass

    x = np.arange(len(data))
    y = data
    # 连续小波变换
    coef,freqs=pywt.cwt(y,np.arange(1,128),'gaus1')
    # 时频(尺度)图
    #plt.matshow( coef ) 
    # 频率
    #plt.plot(freqs)
    


    # learns to repeat simple sequence from random inputs
    # 从随机输入重复简单的序列学习
    np.random.seed(0)

    # parameters for input data dimension and lstm cell count
    # 输入数据维度和lstm单元数量的参数
    mem_cell_ct = 100   # mem_cell_ct是lstm的神经元数目
    x_dim = 50          # x_dim是输入数据的维度
    lstm_param = LstmParam(mem_cell_ct, x_dim)
    lstm_net = LstmNetwork(lstm_param)  
    #y_list = [-0.5, 0.2, 0.1, -0.5]     #此 代码 其是通过自己实现 lstm 网络来逼近一个序列，y_list = [-0.5, 0.2, 0.1, -0.5]                        # 
    y_list = [-0.5, 0, -0.5] 
    input_val_arr = [np.random.random(x_dim) for _ in y_list]   # 输入

    #print(input_val_arr)
    for cur_iter in range(1000):
        print("iter", "%2s" % str(cur_iter), end=": ")
        for ind in range(len(y_list)):
            lstm_net.x_list_add(input_val_arr[ind])

        print("y_pred = [" +
              ", ".join(["% 2.5f" % lstm_net.lstm_node_list[ind].state.h[0] for ind in range(len(y_list))]) +
              "]", end=", ")

        loss = lstm_net.y_list_is(y_list, ToyLossLayer)
        print("loss:", "%.3e" % loss)
        lstm_param.apply_diff(lr=0.1)
        lstm_net.x_list_clear()


def example_2():
    filename = 'data.txt'  #txt文件和当前脚本在同一目录下，所以不用写具体路径
    data = []
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
                pass
            # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            p_tmp = lines.split() 
            data.append(p_tmp[0])  # 添加新读取的数据
            pass

    x = np.arange(len(data))
    y = data
    #print(data)
    # 连续小波变换
    coef,freqs=pywt.cwt(y,np.arange(1,128),'gaus1')
    # 时频(尺度)图
    #plt.matshow(coef) 
    # 频率
    #plt.plot(freqs)
    
    #plt.show()

    f_w = len(coef)  # 频率范围的宽度 
    t = len(coef[0]) # 时间长度 5121
    coef_abs_T = []
    for i in np.arange(t):
        temp = []
        for j in np.arange(f_w):
            temp.append(abs(coef[j][i]))
        coef_abs_T.append(MaxMinNormalization(temp))

    # 频率
    # for i in np.arange(int(t/100+1)):
    #     plt.plot(coef_abs_T[i])

    # 时频(尺度)图
    plt.matshow(coef_abs_T) 
    
    
    plt.show()



def example_3():

    t = np.linspace(-1, 1, 200, endpoint=False)
    sig  = np.cos(2 * np.pi * 7 * t) + np.real(np.exp(-7*(t-0.4)**2)*np.exp(1j*2*np.pi*2*(t-0.4)))
    widths = np.arange(1, 31)
    cwtmatr, freqs = pywt.cwt(sig, widths, 'mexh')
    plt.imshow(cwtmatr, extent=[-1, 1, 1, 31], cmap='PRGn', aspect='auto',
           vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())  
    plt.show() 

    

if __name__ == "__main__":
    example_0()  #
    #example_1()
    #example_3()
        

