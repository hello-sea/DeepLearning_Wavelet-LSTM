# coding:utf-8

import os.path
import sys
import re
import os

import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from sklearn import preprocessing


from MyController import Algorithm_CWT 
from Model.Seg import SegFile

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#python pkl 文件读写
import pickle as pickle

import json
def myJsonLoad(filePath):
    '''把文件打开从字符串转换成数据类型'''
    with open(filePath,'rb') as load_file:
        load_dict = json.load(load_file)
        return load_dict


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



def saveData(py_data, filePath_data, filePath_labels):
    pass
    '''
    with tf.Session() as sess:
        train_data =tf.convert_to_tensor(np.array( trainData.data ) )
    '''
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

def run(filePath_loadData, filePath_data, filePath_labels):

    loadData = eachFile(filePath_loadData) #注意：末尾不加/
    # myReadFile(loadData)  
    # saveData(loadData, filePath_data, filePath_labels)
    
    print(loadData.data_fileName)


def opeanFile(fileName):
    fileName = fileName

    segFile = SegFile()
    
    reply = segFile.loadFile(fileName)
    if(reply != 0):
        print('error!')
    else:
        # cwtmatr,freqs = Algorithm.MyPywtCWT( self.segFile.dataList[ self.segFile.TapeNumCurrent ].data )
        # cwtmatr = Algorithm_CWT.MyScipyCwt(self.segFile.dataList[ self.segFile.TapeNumCurrent ].data, 128)
        print('ok')
        print(len(segFile.dataList[1].data))
        print('ok')
        cwtmatr = Algorithm_CWT.MyWavelets( segFile.dataList[1].data, 128)


        return cwtmatr

def MyPlot(cwtmatr):
    ''' 绘图 '''
    
    print(type(cwtmatr))
    print(len(cwtmatr))
    print(len(cwtmatr[0]))

    # plt.plot(cwtmatr[1])
    # plt.plot(cwtmatr[10])
    # plt.plot(cwtmatr[100])
    
    plt.plot(cwtmatr[1200])
    plt.plot(cwtmatr[1210])
    plt.plot(cwtmatr[1300])
    plt.plot(cwtmatr[1400])
    plt.plot(cwtmatr[1500])

    # plt.plot(cwtmatr[1800])
    # plt.plot(cwtmatr[1900])
    # plt.plot(cwtmatr[2500])

    # plt.matshow(cwtmatr) 
    plt.show() 
    

        
if __name__ == "__main__":
    print('目前系统的编码为：',sys.getdefaultencoding()) 

    ########################################################################
    '''  训练数据生成  '''

    path = 'C:/锚索测量数据库/LSTMs训练数据/' 
    path_TagJson = 'C:/锚索测量数据库/LSTMs训练数据/tag.json'

    TagDict = myJsonLoad(path_TagJson)

    # for i in TagDict:
    #     for j in range(1,5):
    #         print(i['items'][str(j)])
    

    cwtmatr = opeanFile(path + '1.seg')
    cwtmatr = np.array( cwtmatr )
    # Z-Score标准化
    # zscore_scaler = preprocessing.StandardScaler()
    # cwtmatr = zscore_scaler.fit_transform(cwtmatr)

    MyPlot(cwtmatr)

    labels = TagDict[0]['items']
    labels, labels_oneHot = MyLabels( labels )
    plt.plot(labels)
    plt.show() 

    '''
    # import os
    filePath_data = 'tf_model_lstm/train_seg_data.plk'
    if os.path.exists(filePath_data): #删除文件，可使用以下两种方法。
        os.remove(filePath_data)      #os.unlink(my_file)
    
    with open(filePath_data,'wb') as f:
        pickle.dump(cwtmatr, f)


    filePath_labels = 'tf_model_lstm/train_seg_labels.plk'
    if os.path.exists(filePath_labels): #删除文件，可使用以下两种方法。
        os.remove(filePath_labels)      #os.unlink(my_file)

    with open(filePath_labels,'wb') as f:
        pickle.dump(labels_oneHot, f)

    print('\ndone!')

    '''


    # run( path, 'tf_model/train_seg_data.plk', 'tf_model/train_seg_labels.plk')
    #  #注意：path末尾不加/




