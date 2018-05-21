# coding:utf-8

import os.path
import sys
import re
import os
import json

import tensorflow as tf
import numpy as np
from sklearn import preprocessing
import pickle as pickle #python pkl 文件读写

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from Controller import Algorithm_CWT 
from Model.Seg import SegFile


def myJsonLoad(filePath):
    '''把文件打开从字符串转换成数据类型'''
    with open(filePath,'rb') as load_file:
        load_dict = json.load(load_file)
        return load_dict

def MyLabels(Labels):
    returnLabels = []
    returnLabels_oneHot =[]
    # print(type(Labels))
    # print(Labels)
    for i in range(1,4):
        # print(Labels[str(i)])
        # print(Labels[i-1][0], Labels[i-1][1])
        for j in range(Labels[str(i)][0], Labels[str(i)][1]):
            returnLabels.append(i)

            tag = [0,0,0,0]
            tag[i-1] = 1 
            returnLabels_oneHot.append(tag)

    return returnLabels, returnLabels_oneHot


def opeanFile(fileName):
    fileName = fileName

    segFile = SegFile()
    
    reply = segFile.loadFile(fileName)
    if(reply != 0):
        print('error!')
    else:
        # print(len(segFile.dataList[1].data))
        cwtmatr = []
        for i in range(segFile.tapeNum):
            cwtmatr.append(Algorithm_CWT.MyWavelets( segFile.dataList[i].data, 128) )
        return cwtmatr


def MyPlot(cwtmatr):
    ''' 绘图 '''
    
    # print(type(cwtmatr))
    # print(len(cwtmatr))
    # print(len(cwtmatr[0]))

    # plt.plot(cwtmatr[1])
    # plt.plot(cwtmatr[10])
    # plt.plot(cwtmatr[200])
    # plt.plot(cwtmatr[300])
    # plt.plot(cwtmatr[400])
    # plt.plot(cwtmatr[500])
    # plt.plot(cwtmatr[600])
    # plt.plot(cwtmatr[700])
    
    # plt.plot(cwtmatr[1200])
    # plt.plot(cwtmatr[1210])
    # plt.plot(cwtmatr[1300])
    # plt.plot(cwtmatr[1400])
    # plt.plot(cwtmatr[1500])

    # plt.plot(cwtmatr[1800])
    # plt.plot(cwtmatr[1850])
    # plt.plot(cwtmatr[1900])
    # plt.plot(cwtmatr[1950])
    # plt.plot(cwtmatr[2000])
    # plt.plot(cwtmatr[2100])
    # plt.plot(cwtmatr[2300])
    # plt.plot(cwtmatr[2500])

    # plt.matshow(cwtmatr) 
    plt.show() 


def saveData(all_cwtmatr, all_labels_oneHot):
    pass
    # import os
    filePath_data = 'tf_model_lstm/train_seg_data.plk'
    if os.path.exists(filePath_data): #删除文件，可使用以下两种方法。
        os.remove(filePath_data)      #os.unlink(my_file)
    with open(filePath_data,'wb') as f:
        pickle.dump(all_cwtmatr, f)

    filePath_labels = 'tf_model_lstm/train_seg_labels.plk'
    if os.path.exists(filePath_labels): #删除文件，可使用以下两种方法。
        os.remove(filePath_labels)      #os.unlink(my_file)
    with open(filePath_labels,'wb') as f:
        pickle.dump(all_labels_oneHot, f)

def inputData(firstFileNo, lastFileNo):
    # print('目前系统的编码为：',sys.getdefaultencoding()) 

    '''  训练数据生成  '''
    path = 'C:/锚索测量数据库/LSTMs训练数据/' 
    path_TagJson = 'C:/锚索测量数据库/LSTMs训练数据/tag.json'

    TagDict = myJsonLoad(path_TagJson)

    all_cwtmatr = []
    all_labels_oneHot = []

    for number in range(firstFileNo, lastFileNo+1):
        # number = 5 # 1~5
        cwtmatr_cwt = opeanFile(path + str(number)+'.seg')
        for i in range(len(cwtmatr_cwt)):    
            cwtmatr = np.array( cwtmatr_cwt[i] )
            # 逐行 Z-Score 标准化
            cwtmatr = preprocessing.scale(cwtmatr, axis =1)
            all_cwtmatr.append(cwtmatr)
            # MyPlot(cwtmatr)
        
            labels = TagDict[number-1]['items']
            labels, labels_oneHot = MyLabels( labels )
            all_labels_oneHot.append( np.array(labels_oneHot) )
            # plt.plot(labels)

            # plt.show() 

    all_cwtmatr = np.array(all_cwtmatr )
    all_labels_oneHot = np.array(all_labels_oneHot )

    # print(all_cwtmatr.shape)
    # print(all_labels_oneHot.shape)
    # print(all_labels_oneHot[0].shape)
    
    return all_cwtmatr, all_labels_oneHot

if __name__ == "__main__":

    all_cwtmatr, all_labels_oneHot = inputData(4, 5) # number: 1~5
    
    saveData(all_cwtmatr, all_labels_oneHot)

    print('\ndone!')


''' *******************
class MyData():
    def __init__(self):
        self.data_filePath = []
        self.data_fileName = []
        self.data_tpye = []

        self.data = []
        self.labels = []

# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    data = MyData()
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (filepath, allDir))
        if os.path.isfile(child):
            data.data_filePath.append(child)
            data.data_fileName.append(allDir)
            theTpye = re.split('\.',allDir)[0]
            # print(theTpye)
            data.data_tpye.append( theTpye )
    # # 显示
    # for i in array:
    #     print(i)      
    return data

def saveData(py_data, filePath_data, filePath_labels):
    pass
    
    # with tf.Session() as sess:
    #     train_data =tf.convert_to_tensor(np.array( trainData.data ) )
    
    data = np.array( py_data.data )
    labels = py_data.labels

    # import os
    if os.path.exists(filePath_data): #删除文件，可使用以下两种方法。
        os.remove(filePath_data)      #os.unlink(my_file)

    if os.path.exists(filePath_labels): #删除文件，可使用以下两种方法。
        os.remove(filePath_labels)      #os.unlink(my_file)

    with open(filePath_data,'wb') as f:
        pickle.dump(data, f)

    with open(filePath_labels,'wb') as f:
        pickle.dump(labels, f)

    print('\ndone!')

'''