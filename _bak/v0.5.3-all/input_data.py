# coding:utf-8

import os.path
import sys
import re
import os

import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np

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


def myReadFile(py_data):
    # 新建一个Session
    with tf.Session() as sess:

        # path = py_data.data_filePath[0]
        for path in py_data.data_filePath:
            # 读取文件
            image_raw_data = tf.gfile.FastGFile(path, 'rb').read()
            # 解码
            img_data = tf.image.decode_jpeg(image_raw_data)
            # print(img_data)
            # 转灰度图
            # img_data = sess.run(tf.image.rgb_to_grayscale(img_data))  
            # 改变图片尺寸
            resized = tf.image.resize_images(img_data, [28, 28], method=0)
            # 设定 shape
            # resized = tf.reshape(resized, [28, 28, 1]) #最后一维代表通道数目，如果是rgb则为3 
            resized = tf.reshape(resized, [28, 28, 3]) #最后一维代表通道数目，如果是rgb则为3 
            # 标准化
            standardization_image = tf.image.per_image_standardization(resized)#标准化
            # print(standardization_image)
            # print(standardization_image.eval())
            resized = tf.reshape(standardization_image, [-1]) #最后一维代表通道数目，如果是rgb则为3 
            # resized = tf.reshape(resized, [-1]) #最后一维代表通道数目，如果是rgb则为3 

            ## 链接     
            ## resized = tf.expand_dims(resized, 0) # 增加一个维度
            ## print(resized)
            ## print(py_data.data)
            ## test_data = tf.concat(0, [test_data, resized])
            
            py_data.data.append(resized.eval())

        '''
        # #验证数据转换正确
        resized = tf.reshape(py_data.data[0], [28, 28, 3])
        resized = np.asarray(resized.eval(), dtype='uint8')        
        plt.imshow(resized)
        plt.show()
        '''
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

    '''
    trainData = eachFile("../Data/logos/train") #注意：末尾不加/
    # for i in range(0,len(data.data_fileName)):
    #     print(data.data_tpye[i])
    #     print(data.data_oneHot_labels[i])

    myReadFile(trainData)  
    saveData(trainData, 'Model/train_data.plk', 'Model/train_labels.plk')
    
    # print(trainData.data[0].shape)
    # print(trainData.data[0])

    '''

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
        print(type(cwtmatr))
        print(len(cwtmatr))
        print(len(cwtmatr[0]))
        

        
if __name__ == "__main__":
    print('目前系统的编码为：',sys.getdefaultencoding()) 

    ########################################################################
    '''  训练数据生成  '''

    path = 'C:/锚索测量数据库/LSTMs训练数据/' 
    path_TagJson = 'C:/锚索测量数据库/LSTMs训练数据/tag.json'

    TagDict = myJsonLoad(path_TagJson)

    for i in TagDict:
        for j in range(1,5):
            print(i['items'][str(j)])

    opeanFile(path + '1.seg')

    # run( path, 'Model/train_seg_data.plk', 'Model/train_seg_labels.plk')
    #  #注意：path末尾不加/




