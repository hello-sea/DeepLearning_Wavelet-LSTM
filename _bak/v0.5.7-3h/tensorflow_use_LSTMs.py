
from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import pickle as pickle     # python pkl 文件读写

from tensorflow_LSTMs import MyNetworks
from tensorflow_input_data import inputData

'''
def MyPrediction(init_tag, train_data, train_labels, model_path):
    # train_data = np.array( pickle.load( open('tf_model_lstm/train_seg_data.plk', 'rb') ) )
    # train_labels = np.array( pickle.load( open('tf_model_lstm/train_seg_labels.plk', 'rb') ) )
    # model_path = "tf_model_lstm/model.ckpt"

    print( type( train_data ) )     # ndarray
    print( train_data.shape )    
    # for i in range(10):
    #     print(train_labels[i].shape)
    
    #################################################################
    batch_size = len(train_data)
    # Training Parameters:
    learning_rate = 0.05  # 0.1 , 0.001

    # Network Parameters
    num_input = 1
    timesteps = 83 # timesteps
    num_hidden = 200 # hidden layer num of features
    num_classes = 4 # MNIST total classes (1-4 digits)

    # 定义神经网络
    train_op, loss_op, prediction, accuracy, X, Y = MyNetworks(learning_rate, num_input, timesteps, num_hidden, num_classes)

    # 声明tf.train.Saver类用于保存/加载模型
    saver = tf.train.Saver() 

    # Start training
    # 开始训练
    with tf.Session() as sess:

        # 将固化到硬盘中的Session从保存路径再读取出来
        saver.restore(sess, model_path)

        batch_x = train_data
        batch_y = train_labels
            # Reshape data to get 28 seq of 28 elements
        batch_x = batch_x.reshape((batch_size, timesteps, num_input))

        # print("Testing Accuracy(测试集正确率):", \
        #     sess.run(accuracy, feed_dict={X: batch_x, Y: batch_y}))
        

        out = []
        for i in range(batch_size):
            test_data = train_data[i]
            test_label = train_labels[i]
                # Reshape data to get 28 seq of 28 elements
            test_data = test_data.reshape( (1, timesteps, num_input) )

            # print(test_data.shape, test_label)

            # print("分类:", sess.run(prediction, feed_dict={X: test_data}))
            out_tag = sess.run(prediction, feed_dict={X: test_data})
            # 获取矩阵值(概率)最大下标
            j = np.unravel_index( out_tag[0].argmax(), out_tag[0].shape )
            j = j[0]+1
            # print(j)
            out.append(j)

        return out 
'''
class MyPrediction():
    def __init__(self, model_path):
        # model_path = "tf_model_lstm/model.ckpt"

        # Training Parameters:
        self.learning_rate = 0.05  # 0.1 , 0.001

        # Network Parameters
        self.num_input = 1
        self.timesteps = 83 # timesteps
        self.num_hidden = 200 # hidden layer num of features
        self.num_classes = 4 # MNIST total classes (1-4 digits)

        # 定义神经网络
        self.train_op, self.loss_op, self.prediction, self.accuracy, self.X, self.Y = MyNetworks(self.learning_rate, self.num_input, self.timesteps, self.num_hidden, self.num_classes)

        # 声明tf.train.Saver类用于保存/加载模型
        self.saver = tf.train.Saver() 

        # Start training
        # 开始训练

        self.sess = tf.Session()
        # 将固化到硬盘中的Session从保存路径再读取出来
        self.saver.restore(self.sess, model_path)

    def __del__(self):
        self.sess.close()

    def Prediction(self, train_data, train_labels):
        # train_data = np.array( pickle.load( open('tf_model_lstm/train_seg_data.plk', 'rb') ) )
        # train_labels = np.array( pickle.load( open('tf_model_lstm/train_seg_labels.plk', 'rb') ) )
        print( type( train_data ) )     # ndarray
        print( train_data.shape )    
        # for i in range(10):
        #     print(train_labels[i].shape)

        batch_size = len(train_data)

        self.batch_x = train_data
        self.batch_y = train_labels
        self.batch_x = self.batch_x.reshape((batch_size, self.timesteps, self.num_input))

        print("Testing Accuracy(正确率):", \
            self.sess.run(self.accuracy, feed_dict={self.X: self.batch_x, self.Y: self.batch_y}))
        
        out = []
        for i in range(batch_size):
            test_data = train_data[i]
            test_label = train_labels[i]
            test_data = test_data.reshape( (1, self.timesteps, self.num_input) )

            # print(test_data.shape, test_label)
            # print("分类:", sess.run(prediction, feed_dict={X: test_data}))

            out_tag = self.sess.run(self.prediction, feed_dict={self.X: test_data})
            # 获取矩阵值(概率)最大下标
            j = np.unravel_index( out_tag[0].argmax(), out_tag[0].shape )
            out.append( j[0]+1 )
        return out 


import matplotlib.pyplot as plt

if __name__ == "__main__":  
    print('hello!')

    # train_data = np.array( pickle.load( open('tf_model_lstm/train_seg_data.plk', 'rb') ) )
    # train_labels = np.array( pickle.load( open('tf_model_lstm/train_seg_labels.plk', 'rb') ) )

    # train_data, train_labels = inputData(4, 5) # number: 1~5
    # train_data, train_labels = inputData(1, 1) # number: 1~5
    train_data, train_labels = inputData(4, 5) # number: 1~5

    batch_num = len(train_data)
    batch_size = len(train_data[0])

    # 初始化模型
    model_path = "tf_model_lstm/model_1500.ckpt"
    prediction = MyPrediction(model_path)

    for i in range(batch_num):
        out = prediction.Prediction(train_data[i], train_labels[i])
        plt.plot( out )
        plt.show()

    # out = prediction.Prediction( train_data[0], train_labels[0] )
    # plt.plot( out )
    # plt.show()

'''
Figure_4.1_1012_1410_0.866406
Figure_4.2_790_1405_0.786328 *
Figure_4.3_749_1337_0.710156 *
Figure_4.4_812_1728_0.769141 * 
Figure_4.5_270_1501_0.764453 * 
Figure_5.1_379_424_0.701953  *
Figure_5.2_911_1367_0.912109           
Figure_5.3_893_1294_0.935156  
Figure_5.4_1365_1365_0.819922  
Figure_5.5_999_1312_0.825

'''


