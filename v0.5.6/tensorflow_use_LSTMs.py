
from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import pickle as pickle     # python pkl 文件读写

from tensorflow_LSTMs import MyNetworks

def use():
    train_data = np.array( pickle.load( open('tf_model_lstm/train_seg_data.plk', 'rb') ) )
    train_labels = np.array( pickle.load( open('tf_model_lstm/train_seg_labels.plk', 'rb') ) )

    print( type( train_data ) )
    print( train_data.shape )
    # ndarray
    
    ''' ********************************************************************************** '''
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
        saver.restore(sess, "tf_model_lstm/model.ckpt")
   
        batch_x = train_data
        batch_y = train_labels
            # Reshape data to get 28 seq of 28 elements
        batch_x = batch_x.reshape((batch_size, timesteps, num_input))

        print("Testing Accuracy(测试集正确率):", \
            sess.run(accuracy, feed_dict={X: batch_x, Y: batch_y}))
        

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


import matplotlib.pyplot as plt

if __name__ == "__main__":  
    print('hello!')
    out = use()
    
    plt.plot( out )
    plt.show()




